#define pin1 15 // 负责检测低电平的引脚
unsigned long startTime = 0;
unsigned long endTime = 0;
unsigned long sendDelay = 0;
int testInterval = 300;
char data;
int timeout = 200000;

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(pin1, INPUT_PULLUP);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(115200);
  while (!Serial)
  {
    ;
  }
  digitalWrite(LED_BUILTIN, LOW);
}

void loop()
{
  while (digitalRead(pin1))
  {
    ;
    if (Serial.available() > 0)
    {
      data = Serial.read();
      switch (data)
      {
      case 'p':
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
        continue;
      case 'x':
        testInterval = 200;
        break;
      case 'y':
        testInterval = 500;
        break;
      case 'z':
        testInterval = 1500;
        break;
      }
    }
  } // 等待测设备触发
  startTime = micros();
  digitalWrite(LED_BUILTIN, HIGH);
  while (Serial.available() == 0)
  {
    ;
  } // 等待电脑转发设备信息
  switch (Serial.read())
  {
  case 'p':
    endTime = micros();
    break;
  case 'x':
    testInterval = 200;
    return;
  case 'y':
    testInterval = 500;
    return;
  case 'z':
    testInterval = 1500;
    return;
  }
  sendDelay = endTime - startTime;
  Serial.println(sendDelay);
  delay(testInterval);
  digitalWrite(LED_BUILTIN, LOW);
}

void clearSerialBuffer()
{
  while (Serial.available() > 0)
  {
    Serial.read(); // 读取并丢弃一个字节
  }
}

void judgeDate(char data)
{
  switch (data)
  {
  case 'p':
    endTime = micros();
    break;
  case 'x':
    testInterval = 200;
    break;
  case 'y':
    testInterval = 500;
    break;
  case 'z':
    testInterval = 1500;
    break;
  }
}