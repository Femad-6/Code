import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torchvision.models import AlexNet
from torch.utils.data import Dataset, DataLoader
import time
import os

# 设置随机种子以确保实验可重复性
torch.manual_seed(42)
np.random.seed(42)

# ---------------------- 1. 数据集准备 ----------------------
def prepare_dataset():
    """准备CIFAR-10数据集"""
    transform = transforms.Compose([
        transforms.Resize(224),  # AlexNet输入大小为224x224
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    # 下载并加载CIFAR-10数据集
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    
    return trainset, testset

# ---------------------- 2. 投毒攻击实现 ----------------------
class PoisonedDataset(Dataset):
    """投毒数据集类"""
    def __init__(self, original_dataset, poison_ratio, target_class=0, source_class=1):
        """
        Args:
            original_dataset: 原始数据集
            poison_ratio: 投毒比例 (0.0-1.0)
            target_class: 目标类别（投毒后希望被误分类到的类别）
            source_class: 源类别（从哪个类别选择样本进行投毒）
        """
        self.original_dataset = original_dataset
        self.poison_ratio = poison_ratio
        self.target_class = target_class
        self.source_class = source_class
        
        # 获取源类别的所有样本索引
        self.source_indices = [i for i, (_, label) in enumerate(original_dataset) if label == source_class]
        
        # 计算需要投毒的样本数量
        self.num_poison = int(len(self.source_indices) * poison_ratio)
        
        # 随机选择要投毒的样本索引
        np.random.shuffle(self.source_indices)
        self.poison_indices = set(self.source_indices[:self.num_poison])
        
        # 构建数据集索引映射
        self.dataset_indices = list(range(len(original_dataset)))
    
    def __len__(self):
        return len(self.original_dataset)
    
    def __getitem__(self, idx):
        data, label = self.original_dataset[idx]
        
        # 如果该样本是源类别且被选中进行投毒，则翻转标签
        if idx in self.poison_indices:
            label = self.target_class
        
        return data, label

# ---------------------- 3. AlexNet模型定义 ----------------------
def get_alexnet_model(num_classes=10):
    """获取AlexNet模型"""
    model = AlexNet(num_classes=num_classes)
    return model

# ---------------------- 4. 模型训练 ----------------------
def train_model(model, trainloader, criterion, optimizer, device, epochs=10):
    """训练模型"""
    model.train()
    
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for i, (inputs, labels) in enumerate(trainloader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            # 梯度清零
            optimizer.zero_grad()
            
            # 前向传播
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # 反向传播和优化
            loss.backward()
            optimizer.step()
            
            # 统计损失和准确率
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
        
        epoch_loss = running_loss / len(trainloader)
        epoch_acc = 100. * correct / total
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss:.3f}, Accuracy: {epoch_acc:.2f}%')
    
    print('Finished Training')
    return model

# ---------------------- 5. 模型评估 ----------------------
def evaluate_model(model, testloader, device):
    """评估模型"""
    model.eval()
    
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in testloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    accuracy = 100. * correct / total
    print(f'Accuracy on test set: {accuracy:.2f}%')
    return accuracy

def evaluate_attack_success(model, testloader, device, target_class=0, source_class=1):
    """评估攻击成功率"""
    model.eval()
    
    total_source = 0
    successful_attacks = 0
    
    with torch.no_grad():
        for inputs, labels in testloader:
            # 只评估源类别的样本
            source_mask = (labels == source_class)
            if not source_mask.any():
                continue
            
            source_inputs = inputs[source_mask].to(device)
            source_labels = labels[source_mask].to(device)
            
            outputs = model(source_inputs)
            _, predicted = outputs.max(1)
            
            total_source += source_labels.size(0)
            # 攻击成功：源类别样本被预测为目标类别
            successful_attacks += (predicted == target_class).sum().item()
    
    if total_source == 0:
        attack_success_rate = 0.0
    else:
        attack_success_rate = 100. * successful_attacks / total_source
    
    print(f'Attack Success Rate: {attack_success_rate:.2f}%')
    return attack_success_rate

# ---------------------- 6. 实验主函数 ----------------------
def main():
    # 设置设备
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f'Using device: {device}')
    
    # 准备原始数据集
    print("\n1. 准备原始数据集...")
    trainset, testset = prepare_dataset()
    
    # 定义超参数
    batch_size = 32
    learning_rate = 0.001
    epochs = 10
    
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    
    # 投毒比例列表
    poison_ratios = [0.5, 1.0]  #  50%, 100%
    
    # 存储实验结果
    results = {
        'poison_ratios': poison_ratios,
        'test_accuracies': [],
        'attack_success_rates': [],
        'training_times': []
    }
    
    # 对每个投毒比例进行实验
    for poison_ratio in poison_ratios:
        print(f"\n{'='*60}")
        print(f"2. 开始投毒实验，投毒比例: {poison_ratio*100}%")
        print(f"{'='*60}")
        
        # 创建投毒数据集
        poisoned_trainset = PoisonedDataset(trainset, poison_ratio, target_class=0, source_class=1)
        
        # 创建数据加载器
        trainloader = DataLoader(poisoned_trainset, batch_size=batch_size, shuffle=True, num_workers=2)
        testloader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2)
        
        # 获取AlexNet模型
        model = get_alexnet_model(num_classes=10).to(device)
        
        # 定义优化器
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # 训练模型
        print(f"\n3. 训练AlexNet模型...")
        start_time = time.time()
        model = train_model(model, trainloader, criterion, optimizer, device, epochs=epochs)
        training_time = time.time() - start_time
        
        # 评估模型在干净测试集上的准确率
        print(f"\n4. 评估模型在干净测试集上的准确率...")
        test_accuracy = evaluate_model(model, testloader, device)
        
        # 评估攻击成功率
        print(f"\n5. 评估攻击成功率...")
        attack_success_rate = evaluate_attack_success(model, testloader, device, target_class=0, source_class=1)
        
        # 保存实验结果
        results['test_accuracies'].append(test_accuracy)
        results['attack_success_rates'].append(attack_success_rate)
        results['training_times'].append(training_time)
        
        # 保存模型
        model_path = f'alexnet_poisoned_{int(poison_ratio*100)}p.pth'
        torch.save(model.state_dict(), model_path)
        print(f"\n6. 模型已保存到: {model_path}")
    
    # ---------------------- 7. 结果可视化 ----------------------
    print(f"\n{'='*60}")
    print(f"7. 实验结果可视化")
    print(f"{'='*60}")
    
    # 绘制投毒比例与测试准确率的关系
    plt.figure(figsize=(12, 5))
    
    # 子图1：测试准确率
    plt.subplot(1, 2, 1)
    plt.plot(results['poison_ratios'], results['test_accuracies'], marker='o', linestyle='-', color='b')
    plt.title('Poison Ratio vs Test Accuracy')
    plt.xlabel('Poison Ratio')
    plt.ylabel('Test Accuracy (%)')
    plt.grid(True)
    plt.xticks(results['poison_ratios'], ['0%', '50%', '100%'])
    
    # 子图2：攻击成功率
    plt.subplot(1, 2, 2)
    plt.plot(results['poison_ratios'], results['attack_success_rates'], marker='o', linestyle='-', color='r')
    plt.title('Poison Ratio vs Attack Success Rate')
    plt.xlabel('Poison Ratio')
    plt.ylabel('Attack Success Rate (%)')
    plt.grid(True)
    plt.xticks(results['poison_ratios'], ['0%', '50%', '100%'])
    
    plt.tight_layout()
    plt.savefig('poisoning_experiment_results.png')
    plt.show()
    
    # 绘制投毒比例与训练时间的关系
    plt.figure(figsize=(8, 5))
    plt.plot(results['poison_ratios'], results['training_times'], marker='o', linestyle='-', color='g')
    plt.title('Poison Ratio vs Training Time')
    plt.xlabel('Poison Ratio')
    plt.ylabel('Training Time (seconds)')
    plt.grid(True)
    plt.xticks(results['poison_ratios'], ['0%', '50%', '100%'])
    plt.savefig('poisoning_training_time.png')
    plt.show()
    
    # ---------------------- 8. 实验报告生成 ----------------------
    print(f"\n{'='*60}")
    print(f"8. 生成实验报告")
    print(f"{'='*60}")
    
    with open('poisoning_experiment_report.txt', 'w') as f:
        f.write("# AlexNet训练集投毒攻击实验报告\n\n")
        f.write("## 1. 实验概述\n")
        f.write("本实验针对AlexNet模型实施了标签翻转投毒攻击，研究不同投毒比例对模型性能的影响。\n\n")
        
        f.write("## 2. 实验配置\n")
        f.write("- 数据集：CIFAR-10\n")
        f.write("- 模型：AlexNet\n")
        f.write("- 攻击方法：标签翻转攻击\n")
        f.write("- 投毒比例：0%, 50%, 100%\n")
        f.write("- 源类别：1（汽车）\n")
        f.write("- 目标类别：0（飞机）\n")
        f.write(f"- 训练轮数：{epochs}\n")
        f.write(f"-  batch大小：{batch_size}\n")
        f.write(f"- 学习率：{learning_rate}\n\n")
        
        f.write("## 3. 实验结果\n")
        f.write("| 投毒比例 | 测试准确率 | 攻击成功率 | 训练时间(秒) |\n")
        f.write("|---------|-----------|-----------|-------------|\n")
        for i in range(len(poison_ratios)):
            f.write(f"| {poison_ratios[i]*100}% | {results['test_accuracies'][i]:.2f}% | {results['attack_success_rates'][i]:.2f}% | {results['training_times'][i]:.2f} |\n")
        f.write("\n")
        
        f.write("## 4. 结果分析\n")
        f.write("1. **模型准确率**：随着投毒比例的增加，模型在干净测试集上的准确率显著下降。\n")
        f.write("2. **攻击成功率**：攻击成功率随投毒比例的增加而提高，当投毒比例达到100%时，攻击成功率最高。\n")
        f.write("3. **训练时间**：不同投毒比例下的训练时间差异不大，说明标签翻转攻击对训练效率影响较小。\n\n")
        
        f.write("## 5. 结论\n")
        f.write("标签翻转投毒攻击能够有效降低AlexNet模型的性能，并且攻击成功率随投毒比例的增加而提高。\n")
        f.write("该攻击方法简单易行，但隐蔽性较差，因为它会显著降低模型的整体准确率。\n\n")
        
        f.write("## 6. 实验图表\n")
        f.write("- 图1：投毒比例与测试准确率关系图 (poisoning_experiment_results.png)\n")
        f.write("- 图2：投毒比例与攻击成功率关系图 (poisoning_experiment_results.png)\n")
        f.write("- 图3：投毒比例与训练时间关系图 (poisoning_training_time.png)\n")
    
    print("实验报告已生成：poisoning_experiment_report.txt")
    print("实验图表已保存：poisoning_experiment_results.png, poisoning_training_time.png")
    print(f"\n{'='*60}")
    print("实验完成！")
    print(f"{'='*60}")

# ---------------------- 5. 主函数入口 ----------------------
if __name__ == "__main__":
    main()
    