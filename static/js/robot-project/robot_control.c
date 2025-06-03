// robot_control.c
#include <stdio.h>

// 机器人前进
void forward(int speed, int distance) {
    if (speed < 1 || speed > 8) {
        printf("错误: 速度必须在 [1-8] 范围内\n");
        return;
    }
    
    if (distance < 1 || distance > 200) {
        printf("错误: 距离必须在 [1-200] 范围内\n");
        return;
    }
    
    printf("机器人前进: 速度=%d, 距离=%d\n", speed, distance);
    // 实际项目中这里会包含硬件控制代码
}

// 机器人后退
void back(int speed, int distance) {
    if (speed < 1 || speed > 8) {
        printf("错误: 速度必须在 [1-8] 范围内\n");
        return;
    }
    
    if (distance < 1 || distance > 200) {
        printf("错误: 距离必须在 [1-200] 范围内\n");
        return;
    }
    
    printf("机器人后退: 速度=%d, 距离=%d\n", speed, distance);
}

// 机器人左转
void turn_left(int degree) {
    printf("机器人左转: 角度=%d度\n", degree);
}

// 机器人右转
void turn_right(int degree) {
    printf("机器人右转: 角度=%d度\n", degree);
}