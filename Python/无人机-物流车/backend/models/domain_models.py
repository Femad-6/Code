"""
领域模型定义
包含业务实体的核心模型
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import math

class Location:
    """位置类"""
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
    
    def distance_to(self, other: 'Location') -> float:
        """计算到另一个位置的距离(公里)"""
        # 使用Haversine公式计算球面距离
        R = 6371  # 地球半径(公里)
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def __repr__(self):
        return f"Location(lat={self.latitude}, lon={self.longitude})"

class DeliveryPoint:
    """配送点类"""
    def __init__(self, id: int, name: str, address: str, 
                 latitude: float, longitude: float, demand: float = 0.0):
        self.id = id
        self.name = name
        self.address = address
        self.location = Location(latitude, longitude)
        self.demand = demand
        self.status = "active"
    
    def get_distance_to(self, other: 'DeliveryPoint') -> float:
        """计算到另一个配送点的距离"""
        return self.location.distance_to(other.location)
    
    def get_coordinates(self) -> tuple:
        """获取坐标"""
        return (self.location.latitude, self.location.longitude)
    
    def get_location_info(self) -> Dict[str, Any]:
        """获取位置信息"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
            'demand': self.demand
        }
    
    def __repr__(self):
        return f"DeliveryPoint(id={self.id}, name='{self.name}', " \
               f"address='{self.address}', demand={self.demand})"

class Vehicle:
    """车辆类"""
    def __init__(self, id: int, license_plate: str, capacity: float, 
                 max_speed: float, current_location: Optional[Location] = None):
        self.id = id
        self.license_plate = license_plate
        self.capacity = capacity
        self.max_speed = max_speed
        self.current_location = current_location
        self.current_load = 0.0
        self.status = "available"
        self.tasks = []
    
    def add_task(self, task: 'Task'):
        """添加任务"""
        if self.current_load + task.quantity <= self.capacity:
            self.tasks.append(task)
            self.current_load += task.quantity
            return True
        return False
    
    def remove_task(self, task_id: int):
        """移除任务"""
        for task in self.tasks:
            if task.id == task_id:
                self.current_load -= task.quantity
                self.tasks.remove(task)
                break
    
    def is_capacity_full(self) -> bool:
        """检查是否满载"""
        return self.current_load >= self.capacity
    
    def get_remaining_capacity(self) -> float:
        """获取剩余容量"""
        return self.capacity - self.current_load
    
    def reset_vehicle(self):
        """重置车辆状态"""
        self.current_load = 0.0
        self.tasks = []
        self.status = "available"
    
    def __repr__(self):
        return f"Vehicle(id={self.id}, plate='{self.license_plate}', " \
               f"capacity={self.capacity}, load={self.current_load})"

class Drone:
    """无人机类"""
    def __init__(self, id: int, registration_number: str, capacity: float, 
                 max_speed: float, max_range: float, battery_capacity: float,
                 current_location: Optional[Location] = None):
        self.id = id
        self.registration_number = registration_number
        self.capacity = capacity
        self.max_speed = max_speed
        self.max_range = max_range
        self.battery_capacity = battery_capacity
        self.current_location = current_location
        self.current_load = 0.0
        self.current_battery = battery_capacity
        self.status = "available"
        self.tasks = []
    
    def add_task(self, task: 'Task'):
        """添加任务"""
        if self.current_load + task.quantity <= self.capacity:
            self.tasks.append(task)
            self.current_load += task.quantity
            return True
        return False
    
    def remove_task(self, task_id: int):
        """移除任务"""
        for task in self.tasks:
            if task.id == task_id:
                self.current_load -= task.quantity
                self.tasks.remove(task)
                break
    
    def is_capacity_full(self) -> bool:
        """检查是否满载"""
        return self.current_load >= self.capacity
    
    def is_battery_sufficient(self, distance: float) -> bool:
        """检查电池是否足够飞行指定距离"""
        # 简化的电池消耗计算
        battery_consumption = distance * 0.1  # 每公里消耗0.1单位电池
        return self.current_battery >= battery_consumption
    
    def get_remaining_capacity(self) -> float:
        """获取剩余容量"""
        return self.capacity - self.current_load
    
    def get_remaining_battery(self) -> float:
        """获取剩余电池"""
        return self.current_battery
    
    def reset_drone(self):
        """重置无人机状态"""
        self.current_load = 0.0
        self.current_battery = self.battery_capacity
        self.tasks = []
        self.status = "available"
    
    def __repr__(self):
        return f"Drone(id={self.id}, reg='{self.registration_number}', " \
               f"capacity={self.capacity}, battery={self.current_battery})"

class Warehouse:
    """仓库类"""
    def __init__(self, id: int, name: str, address: str, 
                 latitude: float, longitude: float):
        self.id = id
        self.name = name
        self.address = address
        self.location = Location(latitude, longitude)
        self.status = "active"
        self.inventory = {}
    
    def add_inventory(self, item_id: str, quantity: int):
        """添加库存"""
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity
    
    def remove_inventory(self, item_id: str, quantity: int) -> bool:
        """移除库存"""
        if self.inventory.get(item_id, 0) >= quantity:
            self.inventory[item_id] -= quantity
            return True
        return False
    
    def get_inventory(self, item_id: str) -> int:
        """获取库存数量"""
        return self.inventory.get(item_id, 0)
    
    def get_location_info(self) -> Dict[str, Any]:
        """获取位置信息"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
            'inventory': self.inventory
        }
    
    def __repr__(self):
        return f"Warehouse(id={self.id}, name='{self.name}', " \
               f"address='{self.address}')"

class Task:
    """任务类"""
    def __init__(self, id: int, delivery_point_id: int, warehouse_id: int, 
                 quantity: int, priority: int = 0, deadline: Optional[datetime] = None):
        self.id = id
        self.delivery_point_id = delivery_point_id
        self.warehouse_id = warehouse_id
        self.quantity = quantity
        self.priority = priority
        self.deadline = deadline
        self.status = "pending"
        self.assigned_vehicle_id = None
        self.assigned_drone_id = None
        self.route = None
    
    def assign_to_vehicle(self, vehicle_id: int):
        """分配给车辆"""
        self.assigned_vehicle_id = vehicle_id
        self.status = "assigned"
    
    def assign_to_drone(self, drone_id: int):
        """分配给无人机"""
        self.assigned_drone_id = drone_id
        self.status = "assigned"
    
    def complete_task(self):
        """完成任务"""
        self.status = "completed"
    
    def is_overdue(self) -> bool:
        """检查是否超期"""
        if self.deadline:
            return datetime.now() > self.deadline
        return False
    
    def __repr__(self):
        return f"Task(id={self.id}, delivery_point={self.delivery_point_id}, " \
               f"quantity={self.quantity}, status='{self.status}')"

class Route:
    """路线类"""
    def __init__(self, id: int, points: List[DeliveryPoint], warehouse: Warehouse):
        self.id = id
        self.points = points
        self.warehouse = warehouse
        self.distance_matrix = None
        self.optimized = False
        self.total_distance = 0.0
        self.estimated_time = 0.0
    
    def add_point(self, point: DeliveryPoint):
        """添加配送点"""
        self.points.append(point)
        self.optimized = False
    
    def remove_point(self, point: DeliveryPoint):
        """移除配送点"""
        if point in self.points:
            self.points.remove(point)
            self.optimized = False
    
    def update_distance_matrix(self, distance_matrix: List[List[float]]):
        """更新距离矩阵"""
        self.distance_matrix = distance_matrix
        self.optimized = False
    
    def get_distance(self, start_point: DeliveryPoint, end_point: DeliveryPoint) -> Optional[float]:
        """获取两点间距离"""
        if self.distance_matrix is None:
            return start_point.get_distance_to(end_point)
        
        start_idx = self.points.index(start_point)
        end_idx = self.points.index(end_point)
        return self.distance_matrix[start_idx][end_idx]
    
    def calculate_total_distance(self) -> float:
        """计算总距离"""
        if not self.points:
            return 0.0
        
        total_distance = 0.0
        
        # 从仓库到第一个配送点
        if self.points:
            total_distance += self.warehouse.location.distance_to(
                Location(self.points[0].location.latitude, self.points[0].location.longitude)
            )
        
        # 配送点之间的距离
        for i in range(len(self.points) - 1):
            distance = self.get_distance(self.points[i], self.points[i + 1])
            total_distance += distance
        
        # 从最后一个配送点回到仓库
        if self.points:
            total_distance += self.warehouse.location.distance_to(
                Location(self.points[-1].location.latitude, self.points[-1].location.longitude)
            )
        
        self.total_distance = total_distance
        return total_distance
    
    def optimize_route(self):
        """优化路线"""
        # 这里可以集成遗传算法或其他优化算法
        self.optimized = True
        self.calculate_total_distance()
    
    def __repr__(self):
        return f"Route(id={self.id}, points={len(self.points)}, " \
               f"distance={self.total_distance:.2f}km)"



