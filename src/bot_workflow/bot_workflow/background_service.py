import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

from ament_index_python.packages import get_package_share_directory
import json

from ament_index_python.packages import get_package_share_directory
import os
import uuid
from datetime import datetime, timezone
import re
import requests





class Background_service(Node):

    def __init__(self):
        super().__init__('background_service')

        # topics
        self.task_add =  self.create_publisher(String, '/xparo/task/add', 10)
        self.adhaar_detected = self.create_subscription(String,"/adhaar/detected",self.adhaar_detected_fun,10)
        # self.xparo_ask = self.create_publisher(String, '/xparo/ask', 10)
        self.xparo_response = self.create_publisher(String, '/xparo/response', 10)

        # ros2 topic pub /adhaar/detected std_msgs/msg/String '{ "data": "{\"aadhar\": \"123456789012\", \"name\": \"John Doe\", \"age\": 30, \"gender\": \"male\", \"extra_details\": {\"priority\": \"1\", \"status\": \"Pending\", \"title\": \"Doctor Appointment\", \"extraDetails\": {\"temperature\": 36.5}}}"}'

        
        
        ## parameters
        self.service_url= self.declare_parameter('service_url',"https://lazy-legends-robotics.azurewebsites.net/").get_parameter_value().string_value
        self.service_api= self.declare_parameter('service_api',"chatbot_api/pankaj/c736f428-d21c-47c4-8471-c16fc95701d0/").get_parameter_value().string_value
    


    ##################################################
    def adhaar_detected_fun(self, msg):
        data =  json.loads(msg.data)

        check=data.keys()
        timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        timestamp = timestamp.replace("+00:00", "Z")

        ############################
        return_data = {"ADD_services":{
                        "id": str(uuid.uuid4()),
                        "name": "unknown",
                        "age": 0,
                        "aadhar": data["aadhar"],
                        "priority": "3",
                        "gender": "male",
                        "status": "Doctor",
                        "title": "appointment",
                        "extraDetails": {
                            "temperature":30
                        },
                        "created_at": str(timestamp)
                    }}
        ###########################

        if "name" in check:
            return_data["ADD_services"]["name"] = data["name"]
        if "age" in check:
            return_data["ADD_services"]["age"] = data["age"]
        if "gender" in check:
            return_data["ADD_services"]["gender"] = data["gender"]
        if "extra_details" in check:
            dddd = data["extra_details"]
            check_22 = dddd.keys()
            if "priority" in check_22:
                return_data["ADD_services"]["priority"] = dddd["priority"]
            if "status" in check_22:
                return_data["ADD_services"]["status"] = dddd["status"]
            if "title" in check_22:
                return_data["ADD_services"]["title"] = dddd["title"]
            if "extraDetails" in check_22:
                return_data["ADD_services"]["extraDetails"] = dddd["extraDetails"]

        self.send_rest_request_to_task(return_data)




    def send_rest_request_to_task(self,return_data):
        response = requests.post(
                self.service_url+self.service_api, 
                json=return_data,
                headers= {'Content-type': 'application/json'}
                )
        self.get_logger().info(str(response.status_code))









def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Background_service())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
