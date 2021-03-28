# aimbot
射击游戏自动瞄准

基于[centernet]()在win10平台开发。

## 屏幕截取
1. d3dshot : 强大而高效的截屏库，FPS高达60+
2. mss : 跨平台的截屏库
## 模型训练
### 数据集制作
截取了游戏中一部分视频，用于目标标注，类别包括enemy_body, enemy_head, hostage.
其他类别如枪支，药箱等暂未添加

### 训练
backbone用了resnet18，140个epoch

## 操作鼠标
测试了非常多的鼠标控制库，pyautogui没有测试成功，最终用法是鼠标移动和点击分别使用了2个库。

游戏界面分辨率缩放倍数和鼠标移动的位置有关系

## 控制逻辑
优先射击头部，其次身体躯干

## 效果演示
![效果1](.assert/demo-1.gif)



从检测效果来看，centernet对小目标的检测还是挺强的。
完整视频 [知乎](https://www.zhihu.com/column/c_1197285254745030656)
