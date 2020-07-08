#!/usr/bin/env python
# encoding:utf-8
import cv2
import numpy as np
from locator.laser_locator import LaserRectLocator
from locator.box_locator import BoxLaserLocator
from common.geometry_util import *


class LocatorMain():

    def __init__(self):
        self.laser_locator = LaserRectLocator()
        self.box_laser_locator = BoxLaserLocator()

        # 激光中心从传送带到盒子表面的偏移量
        self.offset = np.array([-13.0, 55.0])
        self.laser_rect_area = None
        self.rect_center = None
        self.frame_count = 0

    def run(self, frame):

        # 尝试定位盒子
        box_rst  = self.box_laser_locator.detect(frame)

        img_show = frame.copy()
        h, w, c = img_show.shape
        # 中心画一条线，保证在盒子在中心位置附近
        cv2.line(img_show, (w / 2, 0), (w / 2, h), (50, 255, 50), 1, cv2.LINE_AA)
        cv2.line(img_show, (0, h / 2), (w, h / 2), (255, 50, 255), 1, cv2.LINE_AA)

        scale_factor = 8.5
        screen_center = (w / 2, h / 2)
        refer_rect_width  = 100 * 0.2 * scale_factor
        refer_rect_height = 100 * 0.4 * scale_factor
        # 绘制黄色的矩形框, 要求和目标对齐
        cv2.rectangle(img_show,
                      (int(screen_center[0] - refer_rect_width / 2), int(screen_center[1] - refer_rect_height / 2)),
                      (int(screen_center[0] + refer_rect_width / 2), int(screen_center[1] + refer_rect_height / 2)),
                      (120, 60, 230), 1)

        center_offset = None
        angle_degree = None


        if box_rst is None:
            print "-----------没找到盒子，执行矩形框定位------------"
            # 2. 如果没检测到盒子，先计算矩形框的包容盒，确定中心位置（根据二值化并查找边缘）
            # 根据矩形框和中心构建坐标系，绘制
            # 计算其偏移后的预测位置，绘制
            laser_rect_rst = self.laser_locator.detect(frame)
            if laser_rect_rst is None:
                print "未检测到矩形激光标定目标"
            else:
                laser_rect_area, rect_center = laser_rect_rst

                # 绘制中心和圆环
                cv2.circle(img_show, tuple(np.int0(rect_center)), 4, (0, 0, 255), -1)
                cv2.circle(img_show, tuple(np.int0(rect_center)), 10, (0, 255, 255), 2)
                points = np.int0(laser_rect_area)
                # 绘制最小有向包容盒
                cv2.drawContours(img_show, [points], 0, (0, 255, 255), 2)

                # 更新最新的位置信息
                self.laser_rect_area = laser_rect_area
                self.rect_center = rect_center

        else:
            print "-----------找到盒子，绘制盒子并计算偏移量--------：",
            # 1. 检测到盒子，并计算中点（注意用离中心的偏移量来修正x位置） 如果没有最新的标定数据，则要求其有激光实施标定
            target_rect_area , box_center_float = box_rst
            # 绘制最小有向包容盒
            cv2.drawContours(img_show, [np.int0(target_rect_area)], 0, (0, 0, 255), 2)

            box_center = np.int0(box_center_float)
            # rst_dict 保存了两个点： box_center 是计算出来的盒子中心， laser_circle 激光点中心
            cv2.circle(img_show, tuple(box_center), 10, (0, 200, 0), 2)  # 圆环
            cv2.circle(img_show, tuple(box_center), 3, (100, 100, 0), -1)  # 圆心

            # 计算并绘制预测中点（根据得到的坐标轴）
            if self.rect_center is None:
                print "目前暂未获得激光打标机默认的中心和打印方向信息"
            else:
                r_center = self.rect_center + self.offset

                # 传送带上的中心
                cv2.circle(img_show, tuple(np.int0(self.rect_center)), 4, (0, 0, 255), -1)
                cv2.circle(img_show, tuple(np.int0(self.rect_center)), 10, (0, 255, 255), 2)
                # 绘制中心和圆环, 盒子上的中心
                cv2.circle(img_show, tuple(np.int0(r_center)), 3, (0, 0, 255), -1)
                cv2.circle(img_show, tuple(np.int0(r_center)), 10, (0, 255, 255), 1)
                # 箭头
                cv2.arrowedLine(img_show, tuple(self.rect_center), tuple(np.int0(r_center)), (0, 0, 255), 2)

                # 绘制最小有向包容盒
                laser_rect_area_offset = self.laser_rect_area + self.offset
                r_points = np.int0(laser_rect_area_offset)
                cv2.drawContours(img_show, [r_points], 0, (0, 255, 255), 2)

                # 然后计算偏移后的预测位置和盒子中点的偏移量 ------------------------------------------   1
                cv2.arrowedLine(img_show, tuple(np.int0(r_center)), tuple(np.int0(box_center_float)), (255, 0, 0), 2)
                center_offset = box_center_float - r_center

                # 计算旋转角度            --------------------------------------------------------- 2
                # 激光预测矩形的四个点 laser_rect_area_offset
                # 盒子矩形的四个顶点      target_rect_area

                # 对激光预测矩形进行排序, 绘制向量
                laser_rect_area_offset = sort_rect(laser_rect_area_offset)
                laser_rect_vector_x, laser_rect_vector_y = calc_vector(laser_rect_area_offset)
                cv2.arrowedLine(img_show, tuple(np.int0(laser_rect_area_offset[0])), tuple(np.int0(laser_rect_area_offset[0] + laser_rect_vector_x)),
                                (0, 0, 255), 2, cv2.LINE_AA)
                cv2.arrowedLine(img_show, tuple(np.int0(laser_rect_area_offset[0])), tuple(np.int0(laser_rect_area_offset[0] + laser_rect_vector_y)),
                                (0, 255, 0), 2, cv2.LINE_AA)

                # 对盒子矩形的顶点进行排序显示
                target_rect_area = sort_rect(target_rect_area)
                target_rect_vector_x, target_rect_vector_y = calc_vector(target_rect_area)

                cv2.arrowedLine(img_show, tuple(np.int0(target_rect_area[0])), tuple(np.int0(target_rect_area[0] + target_rect_vector_x)),
                                (0, 0, 255), 2, cv2.LINE_AA)
                cv2.arrowedLine(img_show, tuple(np.int0(target_rect_area[0])), tuple(np.int0(target_rect_area[0] + target_rect_vector_y)),
                                (0, 255, 0), 2, cv2.LINE_AA)

                # 计算Y向量的夹角 laser_rect_vector_y -> target_rect_vector_y

                norm_l = np.linalg.norm(laser_rect_vector_y)
                norm_t = np.linalg.norm(target_rect_vector_y)
                cos_angle = laser_rect_vector_y.dot(target_rect_vector_y) / (norm_l * norm_t)

                angle_radius = np.arccos(cos_angle)
                angle_degree = np.rad2deg(angle_radius)

                print "偏移量：{}, 夹角：{}".format(center_offset, angle_degree)
                # 都记录下来，取一下加权平均数

                # 将像素单位转成物理单位mm

        cv2.imshow("image_final", img_show)

        if center_offset is None or angle_degree is None:
            return None

        # 最后返回偏移量(x,y)和旋转角度Θ
        return center_offset, angle_degree

