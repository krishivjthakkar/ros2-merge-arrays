import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32MultiArray

class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')

        self.array1 = None
        self.array2 = None

        self.sub1 = self.create_subscription(Int32MultiArray, '/input/array1', self.callback1, 10)
        self.sub2 = self.create_subscription(Int32MultiArray, '/input/array2', self.callback2, 10)

        self.publisher = self.create_publisher(Int32MultiArray, '/output/array', 10)

    def callback1(self, msg):
        self.array1 = list(msg.data)
        self.check_and_merge()

    def callback2(self, msg):
        self.array2 = list(msg.data)
        self.check_and_merge()

    def check_and_merge(self):
        if self.array1 is not None and self.array2 is not None:
            merged_list = self.merge_sorted_arrays(self.array1, self.array2)

            output_msg = Int32MultiArray()
            output_msg.data = merged_list

            self.publisher.publish(output_msg)
            self.get_logger().info(f'Published merged array: {merged_list}')

    
    def merge_sorted_arrays(self, arr1, arr2):
        i, j = 0, 0
        merged = []
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                merged.append(arr1[i])
                i += 1
            else:
                merged.append(arr2[j])
                j += 1

        merged.extend(arr1[i:])
        merged.extend(arr2[j:])
        return merged


def main(args=None):
    rclpy.init(args=args)
    node = MergeArraysNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
