#!/usr/bin/env python3
"""
氣球膨脹平滑工具 - 讓3D模型表面更圓滑
支援MagicaVoxel輸出的PLY格式，保持原始結構只修改座標
"""

import argparse
import numpy as np
from pathlib import Path
import logging
from typing import Tuple, Optional
import sys

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 延遲導入，讓錯誤訊息更友好
try:
    import open3d as o3d
    from scipy.spatial import KDTree
except ImportError as e:
    logger.error(f"導入依賴失敗: {e}")
    logger.info("請安裝必要套件: pip install open3d scipy numpy")
    sys.exit(1)


def safe_clone_mesh(mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
    """安全地複製網格，兼容不同版本的 Open3D"""
    # 直接使用最簡單的方式：創建新網格並複製頂點和面
    vertices = np.asarray(mesh.vertices).copy()
    triangles = np.asarray(mesh.triangles).copy()
    
    # 創建新的網格
    new_mesh = o3d.geometry.TriangleMesh()
    new_mesh.vertices = o3d.utility.Vector3dVector(vertices)
    new_mesh.triangles = o3d.utility.Vector3iVector(triangles)
    
    # 我們只關心頂點和面，其他屬性會在處理過程中重新計算
    return new_mesh


class BalloonInflator:
    """氣球膨脹平滑器"""
    
    def __init__(
        self,
        steps: int = 30,
        smooth_per_step: int = 1,
        balloon_strength: float = 0.02,
        preserve_scale: bool = True,
        lambda_param: float = 0.5,
        mu_param: float = -0.53,
        inflation_factor: float = 1.0,
        adaptive_strength: bool = False
    ):
        """
        初始化平滑器
        
        Args:
            steps: 迭代次數
            smooth_per_step: 每次迭代的平滑次數
            balloon_strength: 膨脹強度
            preserve_scale: 是否保持原始尺寸
            lambda_param: Taubin平滑的lambda參數
            mu_param: Taubin平滑的mu參數
            inflation_factor: 膨脹倍率
            adaptive_strength: 是否使用自適應強度（根據頂點曲率）
        """
        self.steps = steps
        self.smooth_per_step = smooth_per_step
        self.balloon_strength = balloon_strength
        self.preserve_scale = preserve_scale
        self.lambda_mu = (lambda_param, mu_param)
        self.inflation_factor = inflation_factor
        self.adaptive_strength = adaptive_strength
        
    def _calculate_curvature_weights(self, mesh: o3d.geometry.TriangleMesh) -> np.ndarray:
        """計算頂點曲率權重（用於自適應膨脹）"""
        vertices = np.asarray(mesh.vertices)
        
        # 簡單的曲率估計：計算每個頂點與鄰居的平均距離
        try:
            mesh.compute_adjacency_list()
            adj_list = mesh.adjacency_list
        except:
            # 如果無法計算鄰接列表，返回均勻權重
            return np.ones(len(vertices))
        
        weights = np.zeros(len(vertices))
        for i, neighbors in enumerate(adj_list):
            if len(neighbors) > 0:
                # 計算頂點到鄰居的平均距離
                distances = np.linalg.norm(
                    vertices[list(neighbors)] - vertices[i], 
                    axis=1
                )
                avg_distance = distances.mean()
                # 距離越大，曲率越小，權重越小
                weights[i] = 1.0 / (1.0 + avg_distance)
        
        # 正規化權重
        if weights.max() > weights.min():
            weights = (weights - weights.min()) / (weights.max() - weights.min())
        
        return weights
    
    def inflate(self, mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
        """
        對網格進行氣球膨脹平滑
        
        Args:
            mesh: Open3D三角網格
            
        Returns:
            平滑後的網格
        """
        # 使用安全的複製方法
        mesh = safe_clone_mesh(mesh)
        
        # 計算原始尺寸用於保持比例
        vertices = np.asarray(mesh.vertices)
        center = vertices.mean(axis=0)
        original_radius = np.linalg.norm(vertices - center, axis=1).mean()
        
        logger.info(f"開始氣球膨脹平滑，迭代次數: {self.steps}")
        
        # 如果需要自適應強度，預先計算權重
        if self.adaptive_strength:
            logger.info("使用自適應膨脹強度")
            curvature_weights = self._calculate_curvature_weights(mesh)
        
        # 主迭代循環
        for step in range(self.steps):
            if step % max(1, self.steps // 10) == 0:
                logger.debug(f"迭代 {step+1}/{self.steps}")
            
            # 1. Taubin平滑
            mesh = mesh.filter_smooth_taubin(
                number_of_iterations=self.smooth_per_step,
                lambda_filter=self.lambda_mu[0],
                mu=self.lambda_mu[1],
            )
            
            # 2. 計算法線並膨脹
            mesh.compute_vertex_normals()
            vertices = np.asarray(mesh.vertices)
            normals = np.asarray(mesh.vertex_normals)
            
            # 應用膨脹
            if self.adaptive_strength:
                # 使用曲率加權的膨脹強度
                local_strength = self.balloon_strength * curvature_weights[:, None]
                vertices += local_strength * normals * self.inflation_factor
            else:
                vertices += self.balloon_strength * normals * self.inflation_factor
            
            # 3. 保持原始尺寸（如果需要）
            if self.preserve_scale:
                current_radius = np.linalg.norm(vertices - center, axis=1).mean()
                if current_radius > 1e-8:
                    scale = original_radius / current_radius
                    vertices = center + (vertices - center) * scale
            
            mesh.vertices = o3d.utility.Vector3dVector(vertices)
        
        mesh.compute_vertex_normals()
        logger.info("平滑完成")
        return mesh


class PLYProcessor:
    """PLY檔案處理器"""
    
    @staticmethod
    def parse_ply_header(lines: list) -> dict:
        """解析PLY檔頭"""
        header_info = {
            'vertex_count': 0,
            'face_count': 0,
            'vertex_start': 0,
            'face_start': 0,
            'has_color': False,
            'format': 'ascii'
        }
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith('element vertex'):
                header_info['vertex_count'] = int(line.split()[2])
            elif line.startswith('element face'):
                header_info['face_count'] = int(line.split()[2])
            elif 'red' in line or 'green' in line or 'blue' in line:
                header_info['has_color'] = True
            elif line.startswith('format'):
                header_info['format'] = line.split()[1]
            elif line == 'end_header':
                header_info['vertex_start'] = i + 1
                header_info['face_start'] = i + 1 + header_info['vertex_count']
                break
        
        return header_info
    
    @staticmethod
    def read_vertices(lines: list, header_info: dict) -> Tuple[np.ndarray, list]:
        """讀取頂點資料"""
        vertices = []
        vertex_lines = []
        
        start = header_info['vertex_start']
        end = start + header_info['vertex_count']
        
        for line in lines[start:end]:
            parts = line.strip().split()
            if len(parts) >= 3:
                x, y, z = map(float, parts[:3])
                vertices.append([x, y, z])
                vertex_lines.append(line)  # 保存原始行
        
        return np.array(vertices), vertex_lines
    
    @staticmethod
    def write_ply_with_new_vertices(
        input_path: Path,
        output_path: Path,
        new_vertices: np.ndarray,
        vertex_lines: list,
        header_info: dict
    ) -> None:
        """將新頂點寫入PLY檔案，保持原始格式"""
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        # 替換頂點行
        vertex_start = header_info['vertex_start']
        for i in range(len(new_vertices)):
            idx = vertex_start + i
            
            # 保留原始行的顏色或其他屬性
            old_parts = vertex_lines[i].strip().split()
            new_xyz = f"{new_vertices[i, 0]:.6f} {new_vertices[i, 1]:.6f} {new_vertices[i, 2]:.6f}"
            
            if len(old_parts) > 3:
                # 保留顏色或其他屬性
                additional_data = " ".join(old_parts[3:])
                lines[idx] = f"{new_xyz} {additional_data}\n"
            else:
                lines[idx] = f"{new_xyz}\n"
        
        # 寫出檔案
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)


def validate_mesh(mesh: o3d.geometry.TriangleMesh) -> bool:
    """驗證網格是否有效"""
    if len(mesh.vertices) == 0:
        logger.error("網格沒有頂點")
        return False
    
    if len(mesh.triangles) == 0:
        logger.error("網格沒有三角面")
        return False
    
    # 檢查NaN值
    vertices = np.asarray(mesh.vertices)
    if np.any(np.isnan(vertices)):
        logger.error("網格包含NaN值")
        return False
    
    return True


def process_mesh(
    input_path: Path,
    output_path: Path,
    inflator: BalloonInflator,
    fix_duplicates: bool = True
) -> bool:
    """
    處理網格檔案的主要流程
    
    Args:
        input_path: 輸入檔案路徑
        output_path: 輸出檔案路徑
        inflator: 膨脹平滑器
        fix_duplicates: 是否修復重複頂點
        
    Returns:
        處理是否成功
    """
    try:
        logger.info(f"讀取檔案: {input_path}")
        
        # 讀取網格
        mesh = o3d.io.read_triangle_mesh(str(input_path))
        
        # 驗證網格
        if not validate_mesh(mesh):
            return False
        
        logger.info(f"網格資訊: 頂點數={len(mesh.vertices)}, 面數={len(mesh.triangles)}")
        
        # 處理重複頂點
        if fix_duplicates:
            logger.info("處理重複頂點...")
            original_vertices = np.asarray(mesh.vertices)
            
            # 移除重複頂點
            mesh.remove_duplicated_vertices()
            mesh.remove_degenerate_triangles()
            
            unique_vertices = np.asarray(mesh.vertices)
            
            # 建立映射
            if len(original_vertices) != len(unique_vertices):
                logger.info(f"移除 {len(original_vertices) - len(unique_vertices)} 個重複頂點")
                
                # 使用KDTree建立原始頂點到唯一頂點的映射
                tree = KDTree(unique_vertices)
                _, vertex_mapping = tree.query(original_vertices)
                
                # 應用膨脹平滑
                logger.info("開始氣球膨脹平滑...")
                smoothed_mesh = inflator.inflate(mesh)
                smoothed_vertices = np.asarray(smoothed_mesh.vertices)
                
                # 映射回原始頂點數量
                final_vertices = smoothed_vertices[vertex_mapping]
            else:
                # 沒有重複頂點，直接處理
                logger.info("開始氣球膨脹平滑...")
                smoothed_mesh = inflator.inflate(mesh)
                final_vertices = np.asarray(smoothed_mesh.vertices)
        else:
            # 不處理重複頂點
            logger.info("開始氣球膨脹平滑（跳過重複頂點處理）...")
            smoothed_mesh = inflator.inflate(mesh)
            final_vertices = np.asarray(smoothed_mesh.vertices)
        
        # 讀取原始PLY檔案結構
        logger.info("讀取原始PLY檔案結構...")
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        header_info = PLYProcessor.parse_ply_header(lines)
        
        if header_info['vertex_count'] != len(final_vertices):
            logger.error(f"頂點數量不匹配: 原始={header_info['vertex_count']}, 新={len(final_vertices)}")
            return False
        
        # 讀取原始頂點行
        _, vertex_lines = PLYProcessor.read_vertices(lines, header_info)
        
        # 寫出新檔案
        logger.info(f"寫入檔案: {output_path}")
        PLYProcessor.write_ply_with_new_vertices(
            input_path, output_path, final_vertices, vertex_lines, header_info
        )
        
        return True
        
    except Exception as e:
        logger.error(f"處理過程中發生錯誤: {e}", exc_info=True)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="氣球膨脹平滑工具 - 讓3D模型表面更圓滑",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  %(prog)s input.ply output.ply
  %(prog)s input.ply output.ply --steps 50 --balloon 0.03
  %(prog)s input.ply output.ply --no-preserve-scale --inflation-factor 1.2
  
適用於MagicaVoxel輸出的PLY格式，保持原始顏色和面結構。
        """
    )
    
    # 必需參數
    parser.add_argument("input", type=Path, help="輸入PLY檔案路徑")
    parser.add_argument("output", type=Path, help="輸出PLY檔案路徑")
    
    # 平滑參數
    parser.add_argument("--steps", type=int, default=30,
                       help="迭代次數 (預設: 30)")
    parser.add_argument("--smooth-per-step", type=int, default=1,
                       help="每輪Taubin平滑迭代次數 (預設: 1)")
    parser.add_argument("--balloon", type=float, default=0.02,
                       help="膨脹強度 (預設: 0.02)")
    
    # 控制參數
    parser.add_argument("--no-preserve-scale", action="store_true",
                       help="不保持原始尺寸，允許模型膨脹")
    parser.add_argument("--inflation-factor", type=float, default=1.0,
                       help="膨脹倍率 (預設: 1.0)")
    parser.add_argument("--lambda", type=float, default=0.5, dest="lambda_param",
                       help="Taubin平滑的lambda參數 (預設: 0.5)")
    parser.add_argument("--mu", type=float, default=-0.53,
                       help="Taubin平滑的mu參數 (預設: -0.53)")
    
    # 進階選項
    parser.add_argument("--adaptive", action="store_true",
                       help="使用自適應膨脹強度（根據曲率）")
    parser.add_argument("--no-fix-duplicates", action="store_true",
                       help="不處理重複頂點（可能影響平滑效果）")
    parser.add_argument("--debug", action="store_true",
                       help="啟用除錯模式，顯示詳細資訊")
    
    args = parser.parse_args()
    
    # 設定日誌等級
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("啟用除錯模式")
    
    # 檢查輸入檔案
    if not args.input.exists():
        logger.error(f"輸入檔案不存在: {args.input}")
        sys.exit(1)
    
    if args.input.suffix.lower() != '.ply':
        logger.warning(f"輸入檔案不是PLY格式: {args.input}")
    
    # 建立膨脹器
    inflator = BalloonInflator(
        steps=args.steps,
        smooth_per_step=args.smooth_per_step,
        balloon_strength=args.balloon,
        preserve_scale=not args.no_preserve_scale,
        lambda_param=args.lambda_param,
        mu_param=args.mu,
        inflation_factor=args.inflation_factor,
        adaptive_strength=args.adaptive
    )
    
    # 處理網格
    success = process_mesh(
        input_path=args.input,
        output_path=args.output,
        inflator=inflator,
        fix_duplicates=not args.no_fix_duplicates
    )
    
    if success:
        logger.info(f"處理完成！輸出檔案: {args.output}")
        
        # 顯示檔案大小比較
        if args.input.exists() and args.output.exists():
            input_size = args.input.stat().st_size / 1024
            output_size = args.output.stat().st_size / 1024
            logger.info(f"檔案大小: 輸入={input_size:.1f}KB, 輸出={output_size:.1f}KB")
    else:
        logger.error("處理失敗！")
        sys.exit(1)


if __name__ == "__main__":
    main()