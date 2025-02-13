import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image 
from std_msgs.msg import String
import cv2
import pytesseract
from pytesseract import Output
import re
import json

from ament_index_python.packages import get_package_share_directory
import os













# Preprocess the image
def preprocess_image(image):
    # Resize the image for better processing
    image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    return binary










class Adhaar_class(Node):

    def __init__(self):
        super().__init__('Adhaar_node')

        self.subscriber = self.create_subscription(Image,'/camera/image_raw',self.process_data,10)
        self.adhaar_detected = self.create_publisher(String,"/adhaar/detected",10)

        self.bridge   = CvBridge()


        ###########################################
        ###########################################
        ###########################################
        # Load Yolo
        weights = os.path.join(get_package_share_directory("adhaar_main","weights","yolov3last2.weights"))
        cfg_file = os.path.join(get_package_share_directory("adhaar_detection","weights","yolov3.cfg"))

        ###########################################
        ###########################################
        ###########################################






    def process_data(self, data): 
        frame = self.bridge.imgmsg_to_cv2(data,'bgr8')


        # Preprocess the image
        processed_image = preprocess_image(frame)

        # Use pytesseract to extract text from the image
        custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_data(processed_image, output_type=Output.DICT, config=custom_config)


        # Combine all text into a single string
        extracted_text = " ".join(details['text'])

        # Print the extracted text for debugging
        print("Extracted Text:", extracted_text)

        # Define regex patterns to extract the required details
        name_pattern = re.compile(r'Name[\s:]*([A-Za-z\s]+)', re.IGNORECASE)
        dob_pattern = re.compile(r'(DOB|Date of Birth)[\s:]*(\d{2}/\d{2}/\d{4})', re.IGNORECASE)
        gender_pattern = re.compile(r'(Gender|Sex)[\s:]*([A-Za-z]+)', re.IGNORECASE)
        aadhar_pattern = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')

        # Extract details using regex
        name = name_pattern.search(extracted_text)
        dob = dob_pattern.search(extracted_text)
        gender = gender_pattern.search(extracted_text)
        aadhar_no = aadhar_pattern.search(extracted_text)

        # Print the extracted details
        print("Name:", name.group(1).strip() if name else "Not found")
        print("DOB:", dob.group(2).strip() if dob else "Not found")
        print("Gender:", gender.group(2).strip() if gender else "Not found")
        print("Aadhaar No:", aadhar_no.group().strip() if aadhar_no else "Not found")


        dta = String()
        dta.data = json.dumps({
            "Name:": name.group(1).strip() if name else "Not found",
            "DOB:": dob.group(2).strip() if dob else "Not found",
            "Gender:": gender.group(2).strip() if gender else "Not found",
            "Aadhaar No:": aadhar_no.group().strip() if aadhar_no else "Not found"
        })


        cv2.imshow("Frame",processed_image)
        cv2.waitKey(1)




def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Adhaar_class())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
