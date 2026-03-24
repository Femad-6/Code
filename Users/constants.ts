import { ResumeData } from './types';

export const RESUME_DATA: ResumeData = {
  name: "李世奇",
  title: "物联网工程技术人员 / 嵌入式软件工程师",
  contact: {
    phone: "18134720693",
    email: "2904532972@qq.com",
    location: "中国, 郑州",
  },
  summary: "专业排名前列 (Top 7%) 的物联网工程本科生，具备扎实的数理基础与嵌入式开发能力。精通 C/C++ 与 STM32 开发，拥有从底层驱动设计到云端数据对接的完整物联网项目经验。曾获多项省级竞赛一等奖，兼具独立钻研精神与团队协作能力，致力于用技术创造实际价值。",
  education: {
    school: "郑州大学",
    degree: "本科",
    major: "物联网工程",
    year: "2023级",
    tags: ["211工程", "双一流建设高校"],
    details: [
      "GPA: 13/182 (前 7%)",
      "核心课程: 嵌入式系统设计、传感器原理、数据结构与算法、计算机网络、无线传感器网络、单片机原理。",
      "荣誉: 郑州大学一等奖学金、校级“三好学生”荣誉称号。"
    ]
  },
  englishLevel: "CET-6 (485分)",
  skills: [
    {
      category: "编程语言",
      items: ["C/C++ (精通/嵌入式主攻)", "Python (数据处理/脚本)", "Java (了解)", "MATLAB"]
    },
    {
      category: "嵌入式/硬件",
      items: ["STM32 HAL库", "51单片机", "Altium Designer (PCB绘制)", "UART/I2C/SPI/CAN", "PWM控制"]
    },
    {
      category: "物联网/通信",
      items: ["MQTT", "CoAP", "HTTP", "ZigBee", "BLE", "Wi-Fi", "LoRa", "阿里云/华为云IoT平台"]
    },
    {
      category: "工具与环境",
      items: ["Keil MDK", "Git/GitHub", "Linux 基础命令", "PyCharm"]
    }
  ],
  interests: [
    "热爱读书 (历史/科技/人文)",
    "打羽毛球 (日常运动)",
    "马拉松 (持有半程马拉松和全程马拉松大众二级证书)"
  ],
  projects: [
    {
      name: "体感手套控制机械臂系统",
      role: "独立开发者 / 项目负责人",
      description: "设计并制造了一款基于MEMS姿态识别的无线体感控制系统，实现人手动作对多自由度机械臂的毫秒级同步控制。",
      techStack: ["STM32", "MPU6050", "卡尔曼滤波", "无线透传", "运动学建模"],
      achievements: [
        "编写底层驱动，利用 DMP 库结合互补滤波算法，实现手部欧拉角的高精度解算。",
        "设计主从机无线通信协议，优化数据包结构，显著降低了传输延迟。",
        "建立机械臂逆运动学模型，将姿态数据映射为PWM信号，解决机械臂抖动问题，抓取成功率 >90%。"
      ]
    },
    {
      name: "智能环境监测系统 (华为杯)",
      role: "核心成员 / 硬件负责人",
      description: "构建了一套集终端采集、边缘计算、云端分析于一体的工业级环境监测解决方案。",
      techStack: ["IoT感知层", "低功耗设计", "网关开发", "华为云IoT"],
      achievements: [
        "主导感知层硬件选型与固件开发，实现了温湿度、光照等多源数据的稳定采集。",
        "协助网关层搭建，设计自适应数据上传策略，系统整体功耗降低约 30%。",
        "荣获省级一等奖，系统在现场演示环节零故障运行，获评委高度评价。"
      ]
    }
  ],
  awards: [
    {
      title: "全国大学生物联网设计竞赛 (华为杯)",
      rank: "省级一等奖",
      description: "核心硬件开发"
    },
    {
      title: "高教社杯全国大学生数学建模竞赛",
      rank: "省级一等奖",
      description: "负责数学建模与 MATLAB 编程实现"
    },
    {
      title: "蓝桥杯全国软件和信息技术专业人才大赛",
      rank: "省级二等奖",
      description: "C/C++ 程序设计组"
    }
  ]
};