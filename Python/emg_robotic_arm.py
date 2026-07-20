#!/usr/bin/env python3
"""
EMG控制机械臂系统
使用肌电信号控制机械臂运动
"""

import time
import threading
import queue
import random
import math
import signal
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
# import numpy as np  # Not needed for this implementation

@dataclass
class EMGSignal:
    """EMG信号数据结构"""
    amplitude: float    # 信号幅度 (0.0 - 1.0)
    frequency: float    # 信号频率 (Hz)
    timestamp: float    # 时间戳
    
    def __init__(self, amplitude: float = 0.0, frequency: float = 0.0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.timestamp = time.time()

@dataclass
class Joint:
    """机械臂关节结构"""
    id: int
    current_angle: float = 0.0      # 当前角度 (度)
    target_angle: float = 0.0       # 目标角度 (度)
    min_angle: float = -180.0       # 最小角度限制
    max_angle: float = 180.0        # 最大角度限制
    speed: float = 30.0             # 运动速度 (度/秒)

class Gesture(Enum):
    """手势识别结果"""
    REST = "休息"
    FIST = "握拳"
    OPEN_HAND = "张手"
    POINT = "指向"
    GRASP = "抓取"
    WAVE = "挥手"

class EMGProcessor:
    """EMG信号处理器"""
    
    def __init__(self, buffer_size: int = 100):
        self.signal_buffer = queue.Queue(maxsize=buffer_size)
        self.buffer_lock = threading.Lock()
        # 简单低通滤波器系数
        self.filter_coeffs = [0.1, 0.2, 0.4, 0.2, 0.1]
    
    def add_signal(self, signal: EMGSignal):
        """添加EMG信号到缓冲区"""
        with self.buffer_lock:
            if self.signal_buffer.full():
                try:
                    self.signal_buffer.get_nowait()  # 移除最老的信号
                except queue.Empty:
                    pass
            self.signal_buffer.put(signal)
    
    def filter_signal(self, raw_data: List[float]) -> float:
        """信号滤波处理"""
        if len(raw_data) < len(self.filter_coeffs):
            return raw_data[-1] if raw_data else 0.0
        
        filtered = 0.0
        for i, coeff in enumerate(self.filter_coeffs):
            filtered += coeff * raw_data[-(i+1)]
        return filtered
    
    def recognize_gesture(self) -> Gesture:
        """手势识别"""
        with self.buffer_lock:
            if self.signal_buffer.empty():
                return Gesture.REST
            
            # 获取最近的信号样本
            signals = []
            temp_queue = queue.Queue()
            
            # 从队列中取出信号进行分析
            while not self.signal_buffer.empty() and len(signals) < 10:
                signal = self.signal_buffer.get()
                signals.append(signal)
                temp_queue.put(signal)
            
            # 将信号放回队列
            while not temp_queue.empty():
                self.signal_buffer.put(temp_queue.get())
            
            if not signals:
                return Gesture.REST
            
            # 计算平均幅度和频率
            avg_amplitude = sum(s.amplitude for s in signals) / len(signals)
            avg_frequency = sum(s.frequency for s in signals) / len(signals)
            
            # 基于幅度和频率的手势识别
            if avg_amplitude < 0.1:
                return Gesture.REST
            elif avg_amplitude > 0.8 and avg_frequency > 50:
                return Gesture.FIST
            elif avg_amplitude > 0.6 and avg_frequency < 30:
                return Gesture.OPEN_HAND
            elif avg_amplitude > 0.4 and avg_frequency > 40:
                return Gesture.GRASP
            elif avg_amplitude > 0.3:
                return Gesture.POINT
            else:
                return Gesture.WAVE

class RoboticArm:
    """机械臂控制系统"""
    
    def __init__(self):
        self.joints = [
            Joint(0, 0.0, 0.0, -180, 180, 45),  # 基座旋转
            Joint(1, 0.0, 0.0, -90, 90, 30),    # 肩部
            Joint(2, 0.0, 0.0, -120, 120, 35),  # 肘部
            Joint(3, 0.0, 0.0, -90, 90, 50),    # 腕部俯仰
            Joint(4, 0.0, 0.0, -180, 180, 60),  # 腕部旋转
            Joint(5, 0.0, 0.0, 0, 90, 40),      # 夹爪
        ]
        self.arm_lock = threading.Lock()
        self.is_moving = False
    
    def set_joint_angle(self, joint_id: int, angle: float):
        """设置关节目标角度"""
        if not (0 <= joint_id < len(self.joints)):
            return
        
        with self.arm_lock:
            joint = self.joints[joint_id]
            joint.target_angle = max(joint.min_angle, min(joint.max_angle, angle))
    
    def execute_gesture(self, gesture: Gesture):
        """执行手势对应的动作"""
        gesture_actions = {
            Gesture.REST: [
                (0, 0),    # 基座
                (1, 0),    # 肩部
                (2, 0),    # 肘部
                (3, 0),    # 腕部俯仰
                (4, 0),    # 腕部旋转
                (5, 0),    # 夹爪打开
            ],
            Gesture.FIST: [
                (1, -30),  # 肩部下压
                (2, 45),   # 肘部弯曲
                (5, 90),   # 夹爪关闭
            ],
            Gesture.OPEN_HAND: [
                (1, 15),   # 肩部上抬
                (2, -20),  # 肘部伸展
                (5, 0),    # 夹爪完全打开
            ],
            Gesture.POINT: [
                (0, 30),   # 基座旋转
                (1, 0),    # 肩部水平
                (2, -45),  # 肘部伸展
                (3, -15),  # 腕部微调
            ],
            Gesture.GRASP: [
                (1, -15),  # 肩部轻微下压
                (2, 30),   # 肘部适度弯曲
                (5, 60),   # 夹爪部分关闭
            ],
            Gesture.WAVE: [
                (0, -30),  # 基座左转
                (1, 30),   # 肩部上抬
                (4, 45),   # 腕部旋转
            ],
        }
        
        actions = gesture_actions.get(gesture, [])
        for joint_id, angle in actions:
            self.set_joint_angle(joint_id, angle)
    
    def update_joints(self):
        """更新关节位置（运动控制）"""
        with self.arm_lock:
            any_moving = False
            delta_time = 0.1  # 100ms更新间隔
            
            for joint in self.joints:
                angle_diff = joint.target_angle - joint.current_angle
                if abs(angle_diff) > 0.5:
                    direction = 1.0 if angle_diff > 0 else -1.0
                    movement = joint.speed * delta_time * direction
                    
                    if abs(movement) > abs(angle_diff):
                        joint.current_angle = joint.target_angle
                    else:
                        joint.current_angle += movement
                    any_moving = True
            
            self.is_moving = any_moving
    
    def print_status(self):
        """打印当前状态"""
        joint_names = ["基座", "肩部", "肘部", "腕俯仰", "腕旋转", "夹爪"]
        
        with self.arm_lock:
            print("机械臂状态:")
            for i, joint in enumerate(self.joints):
                status = f"{joint_names[i]}: {joint.current_angle:.1f}°"
                if abs(joint.current_angle - joint.target_angle) > 0.5:
                    status += f" -> {joint.target_angle:.1f}°"
                print(status)
            
            print(f"运动状态: {'运动中' if self.is_moving else '静止'}")
            print()

class EMGSimulator:
    """EMG信号模拟器"""
    
    def __init__(self):
        random.seed()
    
    def generate_signal(self, target_gesture: Gesture = Gesture.REST) -> EMGSignal:
        """生成模拟EMG信号"""
        gesture_params = {
            Gesture.REST: (0.05, 25.0),
            Gesture.FIST: (0.9, 60.0),
            Gesture.OPEN_HAND: (0.7, 25.0),
            Gesture.POINT: (0.3, 35.0),
            Gesture.GRASP: (0.5, 45.0),
            Gesture.WAVE: (0.4, 30.0),
        }
        
        base_amplitude, base_frequency = gesture_params[target_gesture]
        
        # 添加噪声和变化
        noise = random.uniform(-0.05, 0.05)
        amplitude = max(0.0, min(1.0, base_amplitude + noise))
        frequency = max(10.0, min(100.0, base_frequency + noise * 10))
        
        return EMGSignal(amplitude, frequency)

class EMGRoboticSystem:
    """EMG控制机械臂主系统"""
    
    def __init__(self):
        self.processor = EMGProcessor()
        self.arm = RoboticArm()
        self.simulator = EMGSimulator()
        self.running = False
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n正在关闭系统...")
        self.stop()
        sys.exit(0)
    
    def run(self):
        """运行主系统"""
        print("EMG控制机械臂系统启动...")
        print("系统将模拟EMG信号并控制机械臂运动")
        print("按Ctrl+C退出程序\n")
        
        self.running = True
        
        # 创建线程
        emg_thread = threading.Thread(target=self._emg_acquisition_loop)
        control_thread = threading.Thread(target=self._control_loop)
        motion_thread = threading.Thread(target=self._motion_loop)
        
        # 启动线程
        emg_thread.start()
        control_thread.start()
        motion_thread.start()
        
        # 主循环 - 演示不同手势
        gesture_sequence = [
            Gesture.REST, Gesture.FIST, Gesture.OPEN_HAND,
            Gesture.POINT, Gesture.GRASP, Gesture.WAVE
        ]
        
        current_gesture_idx = 0
        last_gesture_change = time.time()
        
        try:
            while self.running:
                # 每5秒切换一次手势进行演示
                now = time.time()
                if now - last_gesture_change >= 5:
                    current_gesture_idx = (current_gesture_idx + 1) % len(gesture_sequence)
                    last_gesture_change = now
                    current_gesture = gesture_sequence[current_gesture_idx]
                    print(f"切换到手势: {current_gesture.value}")
                
                # 生成对应手势的EMG信号
                signal_data = self.simulator.generate_signal(gesture_sequence[current_gesture_idx])
                self.processor.add_signal(signal_data)
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            self.stop()
        
        # 等待线程结束
        emg_thread.join()
        control_thread.join()
        motion_thread.join()
    
    def stop(self):
        """停止系统"""
        self.running = False
    
    def _emg_acquisition_loop(self):
        """EMG信号采集循环"""
        while self.running:
            # 在实际应用中，这里会从EMG传感器获取真实信号
            time.sleep(0.05)
    
    def _control_loop(self):
        """控制循环"""
        last_gesture = Gesture.REST
        
        while self.running:
            # 识别当前手势
            current_gesture = self.processor.recognize_gesture()
            
            # 如果手势改变，执行相应动作
            if current_gesture != last_gesture:
                print(f"识别手势: {current_gesture.value}")
                self.arm.execute_gesture(current_gesture)
                last_gesture = current_gesture
            
            time.sleep(0.2)
    
    def _motion_loop(self):
        """运动控制循环"""
        last_print = time.time()
        
        while self.running:
            self.arm.update_joints()
            
            # 每2秒打印一次状态
            now = time.time()
            if now - last_print >= 2:
                self.arm.print_status()
                last_print = now
            
            time.sleep(0.1)

def main():
    """主函数"""
    system = EMGRoboticSystem()
    
    try:
        system.run()
    except Exception as e:
        print(f"系统错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())