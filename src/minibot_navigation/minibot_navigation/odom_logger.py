#!/usr/bin/env python3

import csv
import rclpy

from rclpy.node import Node
from nav_msgs.msg import Odometry


class OdomLogger(Node):

    def __init__(self):
        super().__init__('odom_logger')

        self.subscription = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.odom_callback,
            10
        )

        self.csv_file = open('odom_log.csv', 'w', newline='')
        self.writer = csv.writer(self.csv_file)

        self.writer.writerow([
            'time',

            'x',
            'y',
            'z',

            'qx',
            'qy',
            'qz',
            'qw',

            'vx',
            'vy',
            'vz',

            'wx',
            'wy',
            'wz'
        ])

        self.get_logger().info("Logging odometry...")

    def odom_callback(self, msg):

        t = (
            msg.header.stamp.sec +
            msg.header.stamp.nanosec * 1e-9
        )

        self.writer.writerow([

            t,

            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            msg.pose.pose.position.z,

            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w,

            msg.twist.twist.linear.x,
            msg.twist.twist.linear.y,
            msg.twist.twist.linear.z,

            msg.twist.twist.angular.x,
            msg.twist.twist.angular.y,
            msg.twist.twist.angular.z
        ])

        self.csv_file.flush()

    def destroy_node(self):

        self.csv_file.close()

        super().destroy_node()


def main():

    rclpy.init()

    node = OdomLogger()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()