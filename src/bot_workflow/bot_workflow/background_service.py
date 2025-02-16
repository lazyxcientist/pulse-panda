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




class Background_service(Node):

    def __init__(self):
        super().__init__('background_service')

        # topics
        self.task_add =  self.create_publisher(String, '/xparo/task/add', 10)
        self.adhaar_detected = self.create_subscription(String,"/adhaar/detected",self.adhaar_detected_fun,10)
        self.xparo_ask = self.create_publisher(String, '/xparo/ask', 10)
        self.xparo_response = self.create_publisher(String, '/xparo/response', 10)

        
        
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
                        "status": "Todo",
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
            check_22 = data["extra_details"]
            if "priority" in check_22:
                return_data["ADD_services"]["priority"] = data["priority"]
            if "status" in check_22:
                return_data["ADD_services"]["status"] = data["status"]
            if "title" in check_22:
                return_data["ADD_services"]["title"] = data["title"]
            if "extraDetails" in check_22:
                return_data["ADD_services"]["extraDetails"] = data["extraDetails"]

        self.send_rest_request_to_task(return_data)


    def send_rest_request_to_task(self,return_data):
        data =  {
                "id":  str(uuid.uuid4())+str(uuid.uuid4()),
                "avatar": "https://cdn3d.iconscout.com/3d/premium/thumb/male-doctor-eye-test-using-an-chart-3d-illustration-download-in-png-blend-fbx-gltf-file-formats--optical-vision-medical-version-pack-treatment-illustrations-9643496.png?f=webp",
                "content": return_data["ADD_services"]["name"],
                "title": return_data["ADD_services"]["name"],
                "timeout": 80,
                "about": return_data["ADD_services"]["gender"],
                "label": return_data["ADD_services"]["name"],
                "status": "Todo",
                "priority": "3",
                "taskList": [
                {"id": "task-2",
                            "type": "send_rest_request",
                            "title": "Send REST Request", 
                            "extraData": {"url": "http://127.0.0.1:8004/chatbot_api/pankaj/c736f428-d21c-47c4-8471-c16fc95701d0/",
                            "body": json.dumps(return_data),
                            "method": "POST",
                            "headers": {"Content-type": "application/json"}},
                            "on_failure": "",
                            "on_timeout": "",
                            "on_complete": "",
                            "estimatedDuration": 2}
                ],
                "extraDetails": {}
            }
        dd = String()
        dd.data=json.dumps(data)
        self.task_add.publish(dd)
    ##################################################









def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Background_service())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
