"""
请求模型定义
包含所有API请求的数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DeliveryPointRequest(BaseModel):
    """配送点请求模型"""
    id: Optional[int] = None
    name: str = Field(..., description="配送点名称")
    address: str = Field(..., description="配送点地址")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    longitude: float = Field(..., ge=-180, le=180, description="经度")

class VehicleRequest(BaseModel):
    """车辆请求模型"""
    id: Optional[int] = None
    capacity: float = Field(..., gt=0, description="载重能力(kg)")
    max_speed: float = Field(..., gt=0, description="最大速度(km/h)")
    status: str = Field(..., description="车辆状态")

class DroneRequest(BaseModel):
    """无人机请求模型"""
    id: Optional[int] = None
    battery_capacity: float = Field(..., gt=0, description="电池容量(Wh)")
    max_speed: float = Field(..., gt=0, description="最大速度(km/h)")
    status: str = Field(..., description="无人机状态")

class WarehouseRequest(BaseModel):
    """仓库请求模型"""
    id: Optional[int] = None
    name: str = Field(..., description="仓库名称")
    address: str = Field(..., description="仓库地址")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    longitude: float = Field(..., ge=-180, le=180, description="经度")

class TaskRequest(BaseModel):
    """任务请求模型"""
    id: Optional[int] = None
    delivery_point_id: int = Field(..., description="配送点ID")
    quantity: int = Field(..., gt=0, description="配送数量")
    delivery_time: str = Field(..., description="配送时间")

class RouteRequest(BaseModel):
    """路线请求模型"""
    id: Optional[int] = None
    vehicle_id: Optional[int] = None
    drone_id: Optional[int] = None
    status: str = Field(..., description="路线状态")
    delivery_points: List[DeliveryPointRequest] = Field(..., description="配送点列表")

class OptimizationRequest(BaseModel):
    """优化请求模型"""
    vehicles: List[VehicleRequest] = Field(..., description="车辆列表")
    drones: List[DroneRequest] = Field(..., description="无人机列表")
    delivery_points: List[DeliveryPointRequest] = Field(..., description="配送点列表")
    warehouse: WarehouseRequest = Field(..., description="仓库信息")
    tasks: List[TaskRequest] = Field(..., description="任务列表")

class DistanceMatrixRequest(BaseModel):
    """距离矩阵请求模型"""
    points: List[DeliveryPointRequest] = Field(..., description="坐标点列表")

class GeocodingRequest(BaseModel):
    """地理编码请求模型"""
    address: str = Field(..., description="地址")

class AuthenticationRequest(BaseModel):
    """认证请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class UserRequest(BaseModel):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class UpdateRequest(BaseModel):
    """更新请求模型"""
    id: int = Field(..., description="记录ID")
    update_data: dict = Field(..., description="更新数据")

class PaginationRequest(BaseModel):
    """分页请求模型"""
    page: int = Field(..., ge=1, description="页码")
    limit: int = Field(..., ge=1, le=100, description="每页数量")

class FilterRequest(BaseModel):
    """过滤请求模型"""
    filter: dict = Field(..., description="过滤条件")



