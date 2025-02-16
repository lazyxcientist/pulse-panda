#include <Servo.h>

// Define servo objects
Servo neckServo;
Servo leftHandServo;
Servo rightHandServo;

// Define PIR sensor pin
const int pirPin = 2;

// Calibration variables for servos
int neckCalibration = 0;    // Adjust this to calibrate neck servo
int leftHandCalibration = 0; // Adjust this to calibrate left hand servo
int rightHandCalibration = 0; // Adjust this to calibrate right hand servo

// Neutral positions for servos
int neutralNeckPos = 90 + neckCalibration;
int neutralLeftHandPos = 90 + leftHandCalibration;
int neutralRightHandPos = 90 + rightHandCalibration;

// Animation speeds
int animationSpeed = 15; // Delay between each step (in milliseconds)

void setup() {
  // Attach servos to pins
  neckServo.attach(9);
  leftHandServo.attach(10);
  rightHandServo.attach(11);

  // Initialize PIR sensor pin
  pinMode(pirPin, INPUT);

  // Start serial communication
  Serial.begin(9600);

  // Move servos to neutral position at startup
  moveToNeutral();
}

void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any extra whitespace

    if (command == "read_pir") {
      // Read PIR sensor and send the value
      int pirValue = digitalRead(pirPin);
      Serial.println(pirValue);
    } else if (command == "happy") {
      performHappyAnimation();
      Serial.println("true");
    } else if (command == "sad") {
      performSadAnimation();
      Serial.println("true");
    } else if (command == "angry") {
      performAngryAnimation();
      Serial.println("true");
    } else if (command == "confused") {
      performConfusedAnimation();
      Serial.println("true");
    } else if (command == "surprised") {
      performSurprisedAnimation();
      Serial.println("true");
    } else if (command == "fear") {
      performFearAnimation();
      Serial.println("true");
    } else if (command == "bored") {
      performBoredAnimation();
      Serial.println("true");
    } else if (command == "excited") {
      performExcitedAnimation();
      Serial.println("true");
    } else if (command == "anxious") {
      performAnxiousAnimation();
      Serial.println("true");
    } else if (command == "neutral") {
      moveToNeutral();
      Serial.println("true");
    } else {
      Serial.println("false"); // Unknown command
    }
  }
}

// Function to move servos to neutral position
void moveToNeutral() {
  moveServoGradually(neckServo, neckServo.read(), neutralNeckPos);
  moveServoGradually(leftHandServo, leftHandServo.read(), neutralLeftHandPos);
  moveServoGradually(rightHandServo, rightHandServo.read(), neutralRightHandPos);
}

// Function to move a servo gradually from current position to target position
void moveServoGradually(Servo &servo, int currentPos, int targetPos) {
  if (currentPos < targetPos) {
    for (int pos = currentPos; pos <= targetPos; pos++) {
      servo.write(pos);
      delay(animationSpeed);
    }
  } else if (currentPos > targetPos) {
    for (int pos = currentPos; pos >= targetPos; pos--) {
      servo.write(pos);
      delay(animationSpeed);
    }
  }
}

// Animation functions
void performHappyAnimation() {
  // Move neck and hands to happy positions
  moveServoGradually(neckServo, neckServo.read(), 100 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 120 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 60 + rightHandCalibration);
  delay(500); // Hold the position for a moment

  // Wiggle hands to simulate happiness
  for (int i = 0; i < 3; i++) {
    moveServoGradually(leftHandServo, 120 + leftHandCalibration, 100 + leftHandCalibration);
    moveServoGradually(rightHandServo, 60 + rightHandCalibration, 80 + rightHandCalibration);
    delay(200);
    moveServoGradually(leftHandServo, 100 + leftHandCalibration, 120 + leftHandCalibration);
    moveServoGradually(rightHandServo, 80 + rightHandCalibration, 60 + rightHandCalibration);
    delay(200);
  }

  // Return to neutral position
  moveToNeutral();
}

void performSadAnimation() {
  // Move neck and hands to sad positions
  moveServoGradually(neckServo, neckServo.read(), 60 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 90 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 90 + rightHandCalibration);
  delay(1000); // Hold the position for a moment

  // Return to neutral position
  moveToNeutral();
}

void performAngryAnimation() {
  // Move neck and hands to angry positions
  moveServoGradually(neckServo, neckServo.read(), 120 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 60 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 120 + rightHandCalibration);
  delay(500); // Hold the position for a moment

  // Shake hands to simulate anger
  for (int i = 0; i < 3; i++) {
    moveServoGradually(leftHandServo, 60 + leftHandCalibration, 80 + leftHandCalibration);
    moveServoGradually(rightHandServo, 120 + rightHandCalibration, 100 + rightHandCalibration);
    delay(200);
    moveServoGradually(leftHandServo, 80 + leftHandCalibration, 60 + leftHandCalibration);
    moveServoGradually(rightHandServo, 100 + rightHandCalibration, 120 + rightHandCalibration);
    delay(200);
  }

  // Return to neutral position
  moveToNeutral();
}

void performConfusedAnimation() {
  // Move neck and hands to confused positions
  moveServoGradually(neckServo, neckServo.read(), 80 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 70 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 110 + rightHandCalibration);
  delay(1000); // Hold the position for a moment

  // Return to neutral position
  moveToNeutral();
}

void performSurprisedAnimation() {
  // Move neck and hands to surprised positions
  moveServoGradually(neckServo, neckServo.read(), 110 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 180 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 0 + rightHandCalibration);
  delay(500); // Hold the position for a moment

  // Return to neutral position
  moveToNeutral();
}

void performFearAnimation() {
  // Move neck and hands to fear positions
  moveServoGradually(neckServo, neckServo.read(), 45 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 45 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 135 + rightHandCalibration);
  delay(1000); // Hold the position for a moment

  // Return to neutral position
  moveToNeutral();
}

void performBoredAnimation() {
  // Move neck and hands to bored positions
  moveServoGradually(neckServo, neckServo.read(), 90 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 90 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 90 + rightHandCalibration);
  delay(1000); // Hold the position for a moment

  // Return to neutral position
  moveToNeutral();
}

void performExcitedAnimation() {
  // Move neck and hands to excited positions
  moveServoGradually(neckServo, neckServo.read(), 100 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 180 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 0 + rightHandCalibration);
  delay(500); // Hold the position for a moment

  // Wiggle hands to simulate excitement
  for (int i = 0; i < 3; i++) {
    moveServoGradually(leftHandServo, 180 + leftHandCalibration, 160 + leftHandCalibration);
    moveServoGradually(rightHandServo, 0 + rightHandCalibration, 20 + rightHandCalibration);
    delay(200);
    moveServoGradually(leftHandServo, 160 + leftHandCalibration, 180 + leftHandCalibration);
    moveServoGradually(rightHandServo, 20 + rightHandCalibration, 0 + rightHandCalibration);
    delay(200);
  }

  // Return to neutral position
  moveToNeutral();
}

void performAnxiousAnimation() {
  // Move neck and hands to anxious positions
  moveServoGradually(neckServo, neckServo.read(), 70 + neckCalibration);
  moveServoGradually(leftHandServo, leftHandServo.read(), 45 + leftHandCalibration);
  moveServoGradually(rightHandServo, rightHandServo.read(), 135 + rightHandCalibration);
  delay(1000); // Hold the position for a moment

  // Return to neutral position
  moveToNeutral();
}
