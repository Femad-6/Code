#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <chrono>
#include <random>
#include <cmath>
#include <queue>
#include <atomic>
#include <iomanip>
#include <string>
#include <csignal>
#include <algorithm>

using namespace std;

// EMG信号数据结构
struct EMGSignal {
    double amplitude;     // 信号幅度 (0.0 - 1.0)
    double frequency;     // 信号频率 (Hz)
    chrono::steady_clock::time_point timestamp;
    
    EMGSignal(double amp = 0.0, double freq = 0.0) 
        : amplitude(amp), frequency(freq), timestamp(chrono::steady_clock::now()) {}
};

// 机械臂关节结构
struct Joint {
    int id;
    double currentAngle;  // 当前角度 (度)
    double targetAngle;   // 目标角度 (度)
    double minAngle;      // 最小角度限制
    double maxAngle;      // 最大角度限制
    double speed;         // 运动速度 (度/秒)
    
    Joint(int jointId, double minAng, double maxAng, double spd = 30.0) 
        : id(jointId), currentAngle(0.0), targetAngle(0.0), 
          minAngle(minAng), maxAngle(maxAng), speed(spd) {}
};

// 手势识别结果
enum class Gesture {
    REST,           // 休息状态
    FIST,           // 握拳
    OPEN_HAND,      // 张开手掌
    POINT,          // 指向
    GRASP,          // 抓取
    WAVE            // 挥手
};

class EMGProcessor {
private:
    queue<EMGSignal> signalBuffer;
    mutex bufferMutex;
    static const size_t BUFFER_SIZE = 100;
    
    // 信号滤波参数
    vector<double> filterCoeffs = {0.1, 0.2, 0.4, 0.2, 0.1}; // 简单低通滤波器
    
public:
    // 添加EMG信号到缓冲区
    void addSignal(const EMGSignal& signal) {
        lock_guard<mutex> lock(bufferMutex);
        signalBuffer.push(signal);
        
        // 保持缓冲区大小
        if (signalBuffer.size() > BUFFER_SIZE) {
            signalBuffer.pop();
        }
    }
    
    // 信号滤波处理
    double filterSignal(const vector<double>& rawData) {
        if (rawData.size() < filterCoeffs.size()) {
            return rawData.empty() ? 0.0 : rawData.back();
        }
        
        double filtered = 0.0;
        for (size_t i = 0; i < filterCoeffs.size(); ++i) {
            filtered += filterCoeffs[i] * rawData[rawData.size() - 1 - i];
        }
        return filtered;
    }
    
    // 手势识别
    Gesture recognizeGesture() {
        lock_guard<mutex> lock(bufferMutex);
        
        if (signalBuffer.empty()) {
            return Gesture::REST;
        }
        
        // 计算最近信号的平均幅度
        double avgAmplitude = 0.0;
        double avgFrequency = 0.0;
        int count = min(static_cast<int>(signalBuffer.size()), 10);
        
        queue<EMGSignal> temp = signalBuffer;
        vector<EMGSignal> recentSignals;
        
        while (!temp.empty() && recentSignals.size() < count) {
            recentSignals.push_back(temp.front());
            temp.pop();
        }
        
        for (const auto& signal : recentSignals) {
            avgAmplitude += signal.amplitude;
            avgFrequency += signal.frequency;
        }
        
        if (recentSignals.empty()) return Gesture::REST;
        
        avgAmplitude /= recentSignals.size();
        avgFrequency /= recentSignals.size();
        
        // 基于幅度和频率的简单手势识别
        if (avgAmplitude < 0.1) {
            return Gesture::REST;
        } else if (avgAmplitude > 0.8 && avgFrequency > 50) {
            return Gesture::FIST;
        } else if (avgAmplitude > 0.6 && avgFrequency < 30) {
            return Gesture::OPEN_HAND;
        } else if (avgAmplitude > 0.4 && avgFrequency > 40) {
            return Gesture::GRASP;
        } else if (avgAmplitude > 0.3) {
            return Gesture::POINT;
        } else {
            return Gesture::WAVE;
        }
    }
};

class RoboticArm {
private:
    vector<Joint> joints;
    mutex armMutex;
    atomic<bool> isMoving{false};
    
public:
    RoboticArm() {
        // 初始化6自由度机械臂关节
        joints.emplace_back(0, -180, 180, 45);  // 基座旋转
        joints.emplace_back(1, -90, 90, 30);    // 肩部
        joints.emplace_back(2, -120, 120, 35);  // 肘部
        joints.emplace_back(3, -90, 90, 50);    // 腕部俯仰
        joints.emplace_back(4, -180, 180, 60);  // 腕部旋转
        joints.emplace_back(5, 0, 90, 40);      // 夹爪
    }
    
    // 设置关节目标角度
    void setJointAngle(int jointId, double angle) {
        lock_guard<mutex> lock(armMutex);
        if (jointId < 0 || jointId >= joints.size()) return;
        
        Joint& joint = joints[jointId];
        joint.targetAngle = max(joint.minAngle, min(joint.maxAngle, angle));
    }
    
    // 执行手势对应的动作
    void executeGesture(Gesture gesture) {
        switch (gesture) {
            case Gesture::REST:
                // 回到初始位置
                setJointAngle(0, 0);    // 基座
                setJointAngle(1, 0);    // 肩部
                setJointAngle(2, 0);    // 肘部
                setJointAngle(3, 0);    // 腕部俯仰
                setJointAngle(4, 0);    // 腕部旋转
                setJointAngle(5, 0);    // 夹爪打开
                break;
                
            case Gesture::FIST:
                // 紧握动作
                setJointAngle(1, -30);  // 肩部下压
                setJointAngle(2, 45);   // 肘部弯曲
                setJointAngle(5, 90);   // 夹爪关闭
                break;
                
            case Gesture::OPEN_HAND:
                // 张开手掌
                setJointAngle(1, 15);   // 肩部上抬
                setJointAngle(2, -20);  // 肘部伸展
                setJointAngle(5, 0);    // 夹爪完全打开
                break;
                
            case Gesture::POINT:
                // 指向动作
                setJointAngle(0, 30);   // 基座旋转
                setJointAngle(1, 0);    // 肩部水平
                setJointAngle(2, -45);  // 肘部伸展
                setJointAngle(3, -15);  // 腕部微调
                break;
                
            case Gesture::GRASP:
                // 抓取动作
                setJointAngle(1, -15);  // 肩部轻微下压
                setJointAngle(2, 30);   // 肘部适度弯曲
                setJointAngle(5, 60);   // 夹爪部分关闭
                break;
                
            case Gesture::WAVE:
                // 挥手动作
                setJointAngle(0, -30);  // 基座左转
                setJointAngle(1, 30);   // 肩部上抬
                setJointAngle(4, 45);   // 腕部旋转
                break;
        }
    }
    
    // 更新关节位置（运动控制）
    void updateJoints() {
        lock_guard<mutex> lock(armMutex);
        bool anyMoving = false;
        
        for (auto& joint : joints) {
            if (abs(joint.currentAngle - joint.targetAngle) > 0.5) {
                double direction = (joint.targetAngle > joint.currentAngle) ? 1.0 : -1.0;
                double deltaTime = 0.1; // 100ms更新间隔
                double movement = joint.speed * deltaTime * direction;
                
                if (abs(movement) > abs(joint.targetAngle - joint.currentAngle)) {
                    joint.currentAngle = joint.targetAngle;
                } else {
                    joint.currentAngle += movement;
                }
                anyMoving = true;
            }
        }
        
        isMoving = anyMoving;
    }
    
    // 打印当前状态
    void printStatus() {
        lock_guard<mutex> lock(armMutex);
        cout << "机械臂状态:" << endl;
        const vector<string> jointNames = {"基座", "肩部", "肘部", "腕俯仰", "腕旋转", "夹爪"};
        
        for (size_t i = 0; i < joints.size(); ++i) {
            cout << jointNames[i] << ": " 
                 << fixed << setprecision(1) << joints[i].currentAngle << "° ";
            if (abs(joints[i].currentAngle - joints[i].targetAngle) > 0.5) {
                cout << "-> " << joints[i].targetAngle << "°";
            }
            cout << endl;
        }
        cout << "运动状态: " << (isMoving ? "运动中" : "静止") << endl << endl;
    }
};

// EMG信号模拟器
class EMGSimulator {
private:
    random_device rd;
    mt19937 gen;
    uniform_real_distribution<> ampDist;
    uniform_real_distribution<> freqDist;
    uniform_real_distribution<> noiseDist;
    
public:
    EMGSimulator() : gen(rd()), ampDist(0.0, 1.0), freqDist(20.0, 80.0), noiseDist(-0.05, 0.05) {}
    
    // 生成模拟EMG信号
    EMGSignal generateSignal(Gesture targetGesture = Gesture::REST) {
        double baseAmplitude = 0.0;
        double baseFrequency = 25.0;
        
        // 根据目标手势调整基础参数
        switch (targetGesture) {
            case Gesture::REST:
                baseAmplitude = 0.05;
                baseFrequency = 25.0;
                break;
            case Gesture::FIST:
                baseAmplitude = 0.9;
                baseFrequency = 60.0;
                break;
            case Gesture::OPEN_HAND:
                baseAmplitude = 0.7;
                baseFrequency = 25.0;
                break;
            case Gesture::POINT:
                baseAmplitude = 0.3;
                baseFrequency = 35.0;
                break;
            case Gesture::GRASP:
                baseAmplitude = 0.5;
                baseFrequency = 45.0;
                break;
            case Gesture::WAVE:
                baseAmplitude = 0.4;
                baseFrequency = 30.0;
                break;
        }
        
        // 添加噪声和变化
        double amplitude = max(0.0, min(1.0, baseAmplitude + noiseDist(gen)));
        double frequency = max(10.0, min(100.0, baseFrequency + noiseDist(gen) * 10));
        
        return EMGSignal(amplitude, frequency);
    }
};

// 主控制系统
class EMGRoboticSystem {
private:
    EMGProcessor processor;
    RoboticArm arm;
    EMGSimulator simulator;
    atomic<bool> running{true};
    
public:
    void run() {
        cout << "EMG控制机械臂系统启动..." << endl;
        cout << "系统将模拟EMG信号并控制机械臂运动" << endl;
        cout << "按Ctrl+C退出程序" << endl << endl;
        
        // 创建线程
        thread emgThread(&EMGRoboticSystem::emgAcquisitionLoop, this);
        thread controlThread(&EMGRoboticSystem::controlLoop, this);
        thread motionThread(&EMGRoboticSystem::motionLoop, this);
        
        // 主循环 - 用户交互和状态显示
        vector<Gesture> gestureSequence = {
            Gesture::REST, Gesture::FIST, Gesture::OPEN_HAND, 
            Gesture::POINT, Gesture::GRASP, Gesture::WAVE
        };
        
        size_t currentGesture = 0;
        auto lastGestureChange = chrono::steady_clock::now();
        
        while (running) {
            // 每5秒切换一次手势进行演示
            auto now = chrono::steady_clock::now();
            if (chrono::duration_cast<chrono::seconds>(now - lastGestureChange).count() >= 5) {
                currentGesture = (currentGesture + 1) % gestureSequence.size();
                lastGestureChange = now;
                cout << "切换到手势: " << gestureToString(gestureSequence[currentGesture]) << endl;
            }
            
            // 生成对应手势的EMG信号
            EMGSignal signal = simulator.generateSignal(gestureSequence[currentGesture]);
            processor.addSignal(signal);
            
            this_thread::sleep_for(chrono::milliseconds(100));
        }
        
        // 等待线程结束
        emgThread.join();
        controlThread.join();
        motionThread.join();
    }
    
    void stop() {
        running = false;
    }

private:
    void emgAcquisitionLoop() {
        while (running) {
            // 在实际应用中，这里会从EMG传感器获取真实信号
            // 现在使用模拟信号
            this_thread::sleep_for(chrono::milliseconds(50));
        }
    }
    
    void controlLoop() {
        Gesture lastGesture = Gesture::REST;
        
        while (running) {
            // 识别当前手势
            Gesture currentGesture = processor.recognizeGesture();
            
            // 如果手势改变，执行相应动作
            if (currentGesture != lastGesture) {
                cout << "识别手势: " << gestureToString(currentGesture) << endl;
                arm.executeGesture(currentGesture);
                lastGesture = currentGesture;
            }
            
            this_thread::sleep_for(chrono::milliseconds(200));
        }
    }
    
    void motionLoop() {
        while (running) {
            arm.updateJoints();
            
            // 每秒打印一次状态
            static auto lastPrint = chrono::steady_clock::now();
            auto now = chrono::steady_clock::now();
            if (chrono::duration_cast<chrono::seconds>(now - lastPrint).count() >= 2) {
                arm.printStatus();
                lastPrint = now;
            }
            
            this_thread::sleep_for(chrono::milliseconds(100));
        }
    }
    
    string gestureToString(Gesture gesture) {
        switch (gesture) {
            case Gesture::REST: return "休息";
            case Gesture::FIST: return "握拳";
            case Gesture::OPEN_HAND: return "张手";
            case Gesture::POINT: return "指向";
            case Gesture::GRASP: return "抓取";
            case Gesture::WAVE: return "挥手";
            default: return "未知";
        }
    }
};

int main() {
    EMGRoboticSystem system;
    
    // 设置信号处理，优雅退出
    signal(SIGINT, [](int) {
        cout << "\n正在关闭系统..." << endl;
        exit(0);
    });
    
    try {
        system.run();
    } catch (const exception& e) {
        cerr << "系统错误: " << e.what() << endl;
        return 1;
    }
    
    return 0;
}