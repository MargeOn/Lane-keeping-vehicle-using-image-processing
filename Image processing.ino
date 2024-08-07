int x; // giá trị lưu giữ dữ liệu được truyển xuống từ python.
int motorPin1 = 9; // chân 9 điều khiển motor 1 và 2
int motorPin2 = 10; // chân 10 điều khiển motor 1 và 2
int motorPin3 = 11; // chân 11 điều khiển motor 3 và 4
int motorPin4 = 12; // chân 12 điều khiển motor 3 và 4
int motorPWM1 = 5; // chân 5 điều khiển tốc độ motor 1 và 2
int motorPWM2 = 3; // chân 3 điều khiển tốc độ motor 3 và 4
void setup() {
  Serial.begin(115200); // tốc độ truyền bit trên một giây từ python đến arduino.
  Serial.setTimeout(1);
  pinMode(motorPin1, OUTPUT); // đặt trạng thái đầu ra cho chân điều khiển motor 1 và 2 
  pinMode(motorPin2, OUTPUT); // đặt trạng thái đầu ra cho chân điều khiển motor 1 và 2 
  pinMode(motorPWM1, OUTPUT); // đặt trạng thái đâu ra cho chần điều khiển tốc độ motor 1 và 2
  pinMode(motorPin3, OUTPUT); // đặt trạng thái đầu ra cho chân điều khiển motor 3 và 4 
  pinMode(motorPin4, OUTPUT); // đặt trạng thái đầu ra cho chân điều khiển motor 3 và 4 
  pinMode(motorPWM2, OUTPUT); // đặt trạng thái đâu ra cho chần điều khiển tốc độ motor 3 và 4
}
void forward() {
  // Gửi tín hiệu PWM điều khiển tốc độ động cơ để làm xe đi thẳng.
  digitalWrite(motorPin1, HIGH); // chiều quay đi thẳng cho motor 1 và 2
  digitalWrite(motorPin2, LOW); // chiều quay đi thẳng cho motor 1 và 2
  analogWrite(motorPWM1, 50);
  digitalWrite(motorPin3, HIGH); // chiều quay đi thẳng cho motor 3 và 4
  digitalWrite(motorPin4, LOW); // chiều quay đi thẳng cho motor 3 và 4
  analogWrite(motorPWM2, 50); 
}
void left() { 
  digitalWrite(motorPin1, HIGH); // chiều quay đi thẳng cho motor 1 và 2
  digitalWrite(motorPin2, LOW); // chiều quay đi thẳng cho motor 1 và 2
  analogWrite(motorPWM1, 40); 
  digitalWrite(motorPin3, HIGH); // chiều quay đi thẳng cho motor 3 và 4
  digitalWrite(motorPin4, LOW); // chiều quay đi thẳng cho motor 3 và 4
  // Gửi tín hiệu PWM điều khiển tốc độ động cơ để làm xe quay trái.
  analogWrite(motorPWM2, 70); 
}
void right() {
  digitalWrite(motorPin1, HIGH); // chiều quay đi thẳng cho motor 1 và 2
  digitalWrite(motorPin2, LOW); // chiều quay đi thẳng cho motor 1 và 2
  analogWrite(motorPWM1, 70); 
  digitalWrite(motorPin3, HIGH); // chiều quay đi thẳng cho motor 3 và 4
  digitalWrite(motorPin4, LOW); // chiều quay đi thẳng cho motor 3 và 4
  // Gửi tín hiệu PWM điều khiển tốc độ động cơ để làm xe quay phải.
  analogWrite(motorPWM2, 40); 
}
void stop() {
  // đặt trạng thái các chân điều khiển để dừng xe.
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, HIGH);
}
void loop() {
  // Python truyền kiểu dữ liệu dạng chuỗi đến arduino.
  // Từ đó, ta chuyển kiểu chuỗi sang kiểu số nguyên integer.
  x = Serial.readString().toInt();
  // Nếu dữ liệu python gửi đến là 1 thì rẽ phải.
  if (x==1){
   right();
  }
  // Nếu dữ liệu python gửi đến là 1 thì rẽ trái.
  if (x==2) {
   left();
  }
  // Nếu dữ liệu python gửi đến là 3 thì đi thẳng.
  if (x==3) {
   forward();
  }
}


