﻿# codecraft

#### 介绍
华为软件精英挑战赛是华为公司面向在校大学生举办的大型软件竞赛，从2015年至今已成功举办四届。在软件精英挑战赛的舞台上，我们相信您可以充分展示软件设计与编程的能力、享受coding解决问题的乐趣、感受软件改变世界的魅力。 2019届华为软件精英挑战赛赛题为“智能世界•纵横”！

运行仿真图

#!/bin/bash
cd CodeCraft-2019
python src/simulator.py config/car.txt config/road.txt config/cross.txt config/answer.txt



#### 提交日志

时间片在 600秒的时候，任务运行失败

时间片在 800秒的时候，任务运行成功

时间片在700秒的时候，任务运行出错

时间片在790秒的时候，任务运行成功，结果和800秒一致



#### **修改了最短路径算法，引入车道权重**

时间在500秒的时候，任务运行成功

时间片在400秒的时候，任务运行失败



#### **修改最短路径算法，引入了快车道和慢车道**

速度快的车走权值比较高的快车道

速度慢的车走权值比较低的慢车道

时间片在550的时候，达到最优结果  820 + 768

时间片在540的时候，数值和550一致。

时间片在500的时候，发生死锁

创建分支，提交V0.0.2版本



#### **修改时间片大小，根据驶入该终点的车辆进行动态时间片改变**

驶入该终点的车越多，所获得的时间片越大

驶入该终点的车越少，所获得的时间片越小

对于过小的时间片，采用一个固定值时间片为5

时间片设置在 500，固定时间片为 5，达到最优解  730 + 758

时间片设置在 450，固定时间片为 5，发送死锁

时间片设置在 500，固定时间片为 4，发送死锁

创建分支，提交 V0.0.3版本



#### 修改路径算法

以该终点的车发车时，同时把终点设置成起点，将车辆同时发送出去。

设置返回发送车辆的阈值为20

时间片设置450，固定时间片采用递增的方式。 调度时间为：580+595

创建分支，提交 V0.0.4版本



#### 引入西北，东南角法

发车以西北和东南两块区域进行发车

创建分支，提交V0.0.5版本





### 错误路线

终点两两聚类的时候，出现问题，会发生死锁

### 任务安排

1、将相同目的地附近的，都划分为一类 （已完成）

2、最短路径算法，增加权重值

3、将相同终点 并且 以该终点为起点的车，也同时出发

4、将速度不同车辆放在不同的车道行驶，高速车在高速车道，低速车在低速车道

5、随机漫游车道

6、道路分类问题：比如使用了最短路径、权重、频率这三种分类，如果这三种情况的分类有些道路重复了，
那么被重复使用的车道就会变得非常的拥挤，所以我们能不能把道路的分类使用情况是互不重复使用的方式呢？或者减少道路的重复使用率

7、在设计车辆出发点和终点时，能不能先让车道数多的点先出发或先到达呢？