#!/usr/bin/env python3
"""
EMG控制机械臂演示程序
简化版本，用于快速演示系统功能
"""

import time
from emg_robotic_arm import EMGRoboticSystem, Gesture, EMGSimulator, EMGProcessor, RoboticArm

def demo_gesture_sequence():
    """演示所有手势的机械臂动作"""
    print("=== EMG控制机械臂演示程序 ===")
    print("将演示所有6种手势对应的机械臂动作\n")
    
    # 创建系统组件
    arm = RoboticArm()
    simulator = EMGSimulator()
    
    # 手势序列
    gestures = [
        (Gesture.REST, "休息状态 - 回到初始位置"),
        (Gesture.FIST, "握拳动作 - 肩部下压，夹爪关闭"),
        (Gesture.OPEN_HAND, "张手动作 - 肩部上抬，夹爪打开"),
        (Gesture.POINT, "指向动作 - 基座旋转，肘部伸展"),
        (Gesture.GRASP, "抓取动作 - 适度弯曲，夹爪部分关闭"),
        (Gesture.WAVE, "挥手动作 - 基座左转，肩部上抬"),
    ]
    
    print("开始演示，每个动作持续3秒...\n")
    
    for gesture, description in gestures:
        print(f"执行手势: {description}")
        
        # 生成对应的EMG信号
        emg_signal = simulator.generate_signal(gesture)
        print(f"EMG信号 - 幅度: {emg_signal.amplitude:.2f}, 频率: {emg_signal.frequency:.1f}Hz")
        
        # 执行手势动作
        arm.execute_gesture(gesture)
        
        # 模拟运动过程
        for _ in range(30):  # 3秒，每次0.1秒
            arm.update_joints()
            time.sleep(0.1)
        
        # 显示最终状态
        arm.print_status()
        print("-" * 50)
        
        # 稍作停顿
        time.sleep(1)
    
    print("演示完成！")

def interactive_demo():
    """交互式演示"""
    print("=== 交互式EMG控制演示 ===")
    print("输入手势编号来控制机械臂:")
    print("0-休息, 1-握拳, 2-张手, 3-指向, 4-抓取, 5-挥手, q-退出\n")
    
    arm = RoboticArm()
    simulator = EMGSimulator()
    
    gesture_map = {
        '0': Gesture.REST,
        '1': Gesture.FIST,  
        '2': Gesture.OPEN_HAND,
        '3': Gesture.POINT,
        '4': Gesture.GRASP,
        '5': Gesture.WAVE,
    }
    
    gesture_names = {
        '0': '休息',
        '1': '握拳',
        '2': '张手', 
        '3': '指向',
        '4': '抓取',
        '5': '挥手',
    }
    
    try:
        while True:
            user_input = input("请输入手势编号 (0-5) 或 'q' 退出: ").strip().lower()
            
            if user_input == 'q':
                break
            
            if user_input in gesture_map:
                gesture = gesture_map[user_input]
                gesture_name = gesture_names[user_input]
                
                print(f"执行手势: {gesture_name}")
                
                # 生成EMG信号
                emg_signal = simulator.generate_signal(gesture)
                print(f"模拟EMG信号 - 幅度: {emg_signal.amplitude:.2f}, 频率: {emg_signal.frequency:.1f}Hz")
                
                # 执行动作
                arm.execute_gesture(gesture)
                
                # 运动到目标位置
                print("机械臂运动中...")
                for _ in range(30):
                    arm.update_joints()
                    time.sleep(0.1)
                
                # 显示状态
                arm.print_status()
            else:
                print("无效输入，请输入0-5或q")
    
    except KeyboardInterrupt:
        print("\n演示结束")

def signal_analysis_demo():
    """EMG信号分析演示"""
    print("=== EMG信号分析演示 ===")
    print("展示不同手势的EMG信号特征\n")
    
    simulator = EMGSimulator()
    processor = EMGProcessor()
    
    gestures = [Gesture.REST, Gesture.FIST, Gesture.OPEN_HAND, 
                Gesture.POINT, Gesture.GRASP, Gesture.WAVE]
    
    for gesture in gestures:
        print(f"手势: {gesture.value}")
        
        # 生成多个信号样本
        signals = []
        for _ in range(10):
            signal = simulator.generate_signal(gesture)
            signals.append(signal)
            processor.add_signal(signal)
        
        # 计算统计信息
        avg_amp = sum(s.amplitude for s in signals) / len(signals)
        avg_freq = sum(s.frequency for s in signals) / len(signals)
        
        print(f"  平均幅度: {avg_amp:.3f}")
        print(f"  平均频率: {avg_freq:.1f}Hz")
        
        # 测试识别准确性
        recognized = processor.recognize_gesture()
        print(f"  识别结果: {recognized.value}")
        print(f"  识别正确: {'✓' if recognized == gesture else '✗'}")
        print()

if __name__ == "__main__":
    print("EMG控制机械臂演示程序")
    print("=" * 40)
    print("1. 自动演示所有手势")
    print("2. 交互式控制")
    print("3. EMG信号分析")
    print("4. 退出")
    
    try:
        choice = input("\n请选择演示模式 (1-4): ").strip()
        
        if choice == '1':
            demo_gesture_sequence()
        elif choice == '2':
            interactive_demo()
        elif choice == '3':
            signal_analysis_demo()
        elif choice == '4':
            print("退出程序")
        else:
            print("无效选择")
    
    except KeyboardInterrupt:
        print("\n程序被中断")
    except Exception as e:
        print(f"程序错误: {e}")