import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from_class = uic.loadUiType("calculator.ui")[0]


class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calculator")
        
        self.priority = {"+" : 0, "-" : 0, "x" : 1, "/" : 1}
        
        self.input = "0"
        self.prev_input = ""
        self.result = ""
        
        self.init_state = True      # 초기 상태
        self.result_state = False   # 수식이 이전 수식의 결과로 초기화 되어있는 상태
        self.point_state = True     # 소수점 입력 가능 상태
        self.zero_state = True      # 초기 상태 혹은 숫자가 0으로 시작하는 상태
        self.oper_state = True      # 연산자 입력 가능 상태
        self.error_state = False    # 수식 계산 중 에러가 발행한 상태

        
        # 버튼 함수 연결
        self.DIGITBUTTONS = (self.numButton_0, self.numButton_1, self.numButton_2, self.numButton_3, self.numButton_4,
                              self.numButton_5, self.numButton_6, self.numButton_7, self.numButton_8, self.numButton_9)
        self.OPBUTTONS = (self.opButton_eq, self.opButton_plus, self.opButton_minus, self.opButton_mul, self.opButton_div)
        self.CLEARBUTTONS = (self.acButton, self.undoButton)
        
        for numbutton in self.DIGITBUTTONS:
            numbutton.clicked.connect(self.button_Clicked)
        
        for opbutton in self.OPBUTTONS:
            opbutton.clicked.connect(self.button_Clicked)

        self.acButton.clicked.connect(self.button_Clicked)
        self.undoButton.clicked.connect(self.button_Clicked)
        self.pointButton.clicked.connect(self.button_Clicked)

        self.text_current.setText(self.input)


    def button_Clicked(self):
        button = self.sender()

        self.setInitstate()
        self.setResultstate()
        self.setErrorstate()
        self.setOperstate()
        self.setPointstate()
        self.setZerostate()
        
        if button in self.DIGITBUTTONS:                  # 0-9 버튼
            self.digit_Clicked(button)
            self.text_current.setText(self.input)
            self.text_current.append(self.result)
        
        elif button in self.OPBUTTONS[1:]:               # +, -, x, / 버튼
            if self.oper_state == True:
                self.operator_Clicked(button)
                self.text_current.setText(self.input)
                self.text_current.append(self.result)
        
        elif button == self.opButton_eq:                 # = 버튼
            if self.init_state == False and self.result_state == False and self.error_state == False:
                self.equal_Clicked()
                self.text_current.setText(self.prev_input)
                self.text_current.append(self.result)
                
        
        elif button == self.acButton:                    # AC 버튼
            self.ac_Clicked()
            self.text_current.setText(self.input)
            self.text_current.append(self.result)
        
        elif button == self.undoButton:                  # C 버튼
            if self.result_state == False:
                self.undo_Clicked()
                self.text_current.setText(self.input)
                self.text_current.append(self.result)
        
        else:
            if self.point_state == True:                 # .(소수점) 버튼
                self.point_Clicked()            
                self.text_current.setText(self.input)
                self.text_current.append(self.result)
        
    

    def setInitstate(self):
        self.init_state = True if self.input == "0" else False



    # 수식이 이전 수식의 결과로 초기화 되어있는 상태
    def setResultstate(self):
        self.result_state = True if self.result != "" else False



    # self.error_state = True : 계산 에러가 발생한 상태
    def setErrorstate(self):
        if self.result == "계산할 수 없는 수식입니다.":
            self.error_state = True
        else:
            self.error_state = False

    

    # self.oper_state = True : 연산자 입력 가능 상태
    def setOperstate(self):
        # input가 초기 상태 or 마지막 입력이 연산자인 상태 or 에러 발생 상태
        if self.init_state or self.input[-1] in self.priority.keys() or self.error_state == True:
            self.oper_state = False
        else:
            self.oper_state = True
        


    # self.point_state = True : 소수점 입력 가능 상태
    def setPointstate(self):
        for i in self.input[::-1]:                         # input를 역순으로 탐색
            if i == ".":                                   # 소수점이 이미 있으면 point_state = False & 종료
                self.point_state = False
                return
            else:
                self.point_state = True
            if i in self.priority.keys():                   # 연산자를 만나면 조기 종료
                return
        
    

    # self.zero_state = True : 수식이 초기 상태 or 연산자 바로 다음에 0이 있는 상태
    def setZerostate(self):
        if self.init_state or (self.input[-1] == "0" and self.input[-2] in self.priority.keys()):
            self.zero_state = True
        else:
            self.zero_state = False
        
    

    # 숫자: 1-9 버튼
    def digit_Clicked(self, button):
        if button == self.numButton_0: new_digit = "0"
        elif button == self.numButton_1: new_digit = "1"
        elif button == self.numButton_2: new_digit = "2"
        elif button == self.numButton_3: new_digit = "3"
        elif button == self.numButton_4: new_digit = "4"
        elif button == self.numButton_5: new_digit = "5"
        elif button == self.numButton_6: new_digit = "6"
        elif button == self.numButton_7: new_digit = "7"
        elif button == self.numButton_8: new_digit = "8"
        else: new_digit = "9"
        
        if self.result_state == True:                       # 결과가 계산된 상태이면 
            self.text_history.append("")                    # 숫자 버튼을 눌렀을 때 이전 수식 & 결과를 히르토리 창에 출력
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
            self.result = ""                                # 결과 값 초기화
            self.input = new_digit
        
        elif self.zero_state:                               # 수식이 초기 상태 or 연산자 바로 다음에 0이 있는 상태
            self.input = self.input[:-1]
            self.input += new_digit
        
        else:
            self.input += new_digit
    


    # 사칙연산자: +, -, x, / 버튼
    # oper_state = True이면, 연산자를 input 추가한다.
    def operator_Clicked(self, button):            
        if button == self.opButton_plus: new_oper = "+"
        elif button == self.opButton_minus: new_oper = "-"
        elif button == self.opButton_mul: new_oper = "x"
        else: new_oper = "/"

        if self.result_state == True: 
            self.text_history.append("")
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
            self.result = ""
            
        self.input += new_oper  

    

    def equal_Clicked(self):
        try:
            res = eval(self.input.replace("x", "*"))
            
            if res == int(res):
                self.result = str(int(res))
            else:
                self.result = str(res)
            
            self.error_state = False
        
        except:
            self.result = "계산할 수 없는 수식입니다."
        
        self.prev_input = self.input

        if self.error_state == False:
            self.input = self.result
    


    def point_Clicked(self):
        new_digit = "."
        if self.result_state == True:
            self.text_history.append("")
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
            self.result = ""
        self.input += new_digit
    


    def ac_Clicked(self):
        if self.result_state:
            self.text_history.append("")
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
        self.input = "0"
        self.result = ""
    
    

    def undo_Clicked(self):
        if len(self.input) > 1:
            self.input = self.input[:-1]
        else:
            self.input = "0"

            

    def inToPost(self, input):
        postfix = []
        operators = []
        num = ''
        
        for i in input:
            if i not in self.priority.keys():
                num += i
            else:
                postfix.append(num)
                num = ''
                
                if len(operators) == 0 or self.priority[i] > self.priority[operators[-1]]:
                    operators.append(i)
                else:
                    while len(operators) != 0 and self.priority[i] <= self.priority[operators[-1]]:
                        postfix.append(operators.pop())      
                    operators.append(i)
        
        postfix.append(num)
        while len(operators) != 0:
            postfix.append(operators.pop())
        
        return postfix

    

    def getResult(self, postfix):
        operands = []
        for i in postfix:
            if i not in self.priority.keys():
                operands.append(i)
            else:
                second = operands.pop()
                first = operands.pop()
        
                if i == '+':
                    try: result = float(first) + float(second)
                    except: result = "계산할 수 없는 수식입니다."
                elif i == '-':
                    try: result = float(first) - float(second)
                    except: result = "계산할 수 없는 수식입니다."
                elif i == 'x':
                    try: result = float(first) * float(second)
                    except: result = "계산할 수 없는 수식입니다."  
                else:
                    try: result = float(first) / float(second)
                    except: result = "계산할 수 없는 수식입니다."
                
                operands.append(str(result))

        return operands.pop()
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())



########## 출 력 ###########
# if button == self.opButton_eq:
#     if self.error_state == False:
#         self.text_current.setText(self.input)
#         self.text_current.append(self.result)
#         self.input = self.result

# elif button == self.undoButton:
#     if self.result_state:
#         self.text_current.setText(self.prev_input)
#         self.text_current.append(self.result)
#     else:
#         self.text_current.setText(self.input)

# elif button == self.pointButton:
#     if self.result_state == False:
#         self.text_current.setText(self.input)

# else:
#     self.text_current.setText(self.input)

# self.text_current.setText(self.input)
# self.text_current.append(self.result)
# if button == self.opButton_eq:
#     if self.error_state == False:
#         self.input = self.result