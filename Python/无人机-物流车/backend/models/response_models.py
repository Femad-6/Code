"""
响应模型定义
包含所有API响应的数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DeliveryPointResponse(BaseModel):
    """配送点响应模型"""
    id: int = Field(..., description="配送点ID")
    name: str = Field(..., description="配送点名称")
    address: str = Field(..., description="配送点地址")
    coordinates: Optional[List[float]] = Field(default=None, description="坐标[经度, 纬度]")
    status: str = Field(default="active", description="状态")

class VehicleResponse(BaseModel):
    """车辆响应模型"""
    id: int = Field(..., description="车辆ID")
    license_plate: str = Field(..., description="车牌号")
    capacity: float = Field(..., description="载重能力(kg)")
    max_speed: float = Field(..., description="最大速度(km/h)")
    status: str = Field(default="active", description="状态")

class DroneResponse(BaseModel):
    """无人机响应模型"""
    id: int = Field(..., description="无人机ID")
    registration_number: str = Field(..., description="注册号")
    capacity: float = Field(..., description="载重能力(kg)")
    max_speed: float = Field(..., description="最大速度(km/h)")
    max_range: float = Field(..., description="最大航程(km)")
    status: str = Field(default="active", description="状态")

class WarehouseResponse(BaseModel):
    """仓库响应模型"""
    id: int = Field(..., description="仓库ID")
    name: str = Field(..., description="仓库名称")
    address: str = Field(..., description="仓库地址")
    coordinates: Optional[List[float]] = Field(default=None, description="坐标[经度, 纬度]")
    status: str = Field(default="active", description="状态")

class TaskResponse(BaseModel):
    """任务响应模型"""
    id: int = Field(..., description="任务ID")
    delivery_point_id: int = Field(..., description="配送点ID")
    warehouse_id: int = Field(..., description="仓库ID")
    quantity: int = Field(..., description="配送数量")
    priority: int = Field(default=0, description="优先级")

class RouteResponse(BaseModel):
    """路线响应模型"""
    id: int = Field(..., description="路线ID")
    route_id: int = Field(..., description="路线编号")
    vehicle_id: int = Field(..., description="车辆ID")
    drone_id: int = Field(..., description="无人机ID")
    start_time: Optional[str] = Field(default=None, description="开始时间")
    end_time: Optional[str] = Field(default=None, description="结束时间")
    status: str = Field(default="planned", description="状态")

class OptimizationResultResponse(BaseModel):
    """优化结果响应模型"""
    best_solution: Dict[str, Any] = Field(..., description="最优解")
    best_cost: float = Field(..., description="最优成本")
    best_route: Optional[Dict[str, Any]] = Field(default=None, description="最优路线")
    execution_time: float = Field(..., description="执行时间(秒)")

class AuthResponse(BaseModel):
    """认证响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    token: Optional[str] = Field(default=None, description="认证令牌")
    
    @property
    def response(self):
        """返回响应字典"""
        return {
            "success": self.success,
            "message": self.message,
            "token": self.token
        }

class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = Field(default=False, description="是否成功")
    message: str = Field(..., description="错误消息")
    error_code: Optional[str] = Field(default=None, description="错误代码")
    
    @property
    def response(self):
        """返回响应字典"""
        return {
            "success": self.success,
            "message": self.message,
            "error_code": self.error_code
        }

class PaginationResponse(BaseModel):
    """分页响应模型"""
    data: List[Any] = Field(..., description="数据列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    limit: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")

class DistanceResponse(BaseModel):
    """距离响应模型"""
    distance: float = Field(..., description="距离(km)")
    duration: float = Field(..., description="预计时间(分钟)")

class GeocodingResponse(BaseModel):
    """地理编码响应模型"""
    latitude: float = Field(..., description="纬度")
    longitude: float = Field(..., description="经度")
    address: str = Field(..., description="地址")
    formatted_address: Optional[str] = Field(default=None, description="格式化地址")



