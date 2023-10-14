from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic


from_class = uic.loadUiType("./src/calculator.ui")[0]


class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calculator")
        
        self.input = "0"
        self.prev_input = ""
        self.result = ""
        self.op = "+-x/"
        self.parStack = []
        
        self.init_state = True                                  # 초기 상태
        self.result_state = False                               # 수식이 이전 수식의 결과로 초기화 되어있는 상태
        self.point_state = True                                 # 소수점 입력 가능 상태
        self.zero_state = True                                  # 초기 상태 혹은 마지막 숫자가 0으로 시작하는 상태
        self.oper_state = True                                  # 사칙 연산자 입력 가능 상태
        self.eq_state = True                                    # 등호 연산자 입력 가능 상태
        self.error_state = False                                # 수식 계산 중 에러가 발행한 상태
        self.par_state = {"open" : True, "close" : False}       # open : "("" 사용 가능 상태, close : ")" 사용 가능 상태

        self.DIGITBUTTONS = (self.numButton_0, self.numButton_1, self.numButton_2, self.numButton_3, self.numButton_4,
                              self.numButton_5, self.numButton_6, self.numButton_7, self.numButton_8, self.numButton_9)
        self.OPBUTTONS = (self.opButton_eq, self.opButton_plus, self.opButton_minus, self.opButton_mul, self.opButton_div)
        self.CLEARBUTTONS = (self.acButton, self.undoButton)
        self.PARENTHESIS = (self.parButton_open, self.parButton_close)
        
        for numbutton in self.DIGITBUTTONS:
            numbutton.clicked.connect(self.button_Clicked)
        
        for opbutton in self.OPBUTTONS:
            opbutton.clicked.connect(self.button_Clicked)
        
        for parbutton in self.PARENTHESIS:
            parbutton.clicked.connect(self.button_Clicked)

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
        self.setParstate()
        self.setEqstate()
        
        if button in self.DIGITBUTTONS:                  # 0-9 버튼
            self.digit_Clicked(button)
            self.text_current.setText(self.input)
            self.text_current.append(self.result)
        
        elif button in self.OPBUTTONS[1:]:               # +, -, x, / 버튼
            if self.oper_state == True:
                self.operator_Clicked(button)
                self.text_current.setText(self.input)
                self.text_current.append(self.result)

        elif button in self.PARENTHESIS:                # (, ) 버튼
            if button == self.parButton_open:
                if self.par_state["open"] == True:
                    self.openPar_Clicked()
                    self.text_current.setText(self.input)
                    self.text_current.append(self.result)
            else:
                if self.par_state["close"] == True:
                    self.closePar_Clicked()
                    self.text_current.setText(self.input)
                    self.text_current.append(self.result)
        
        elif button == self.opButton_eq:                 # = 버튼
            if self.eq_state:
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
        if self.input == "0": 
            self.init_state = True 
        else: 
            self.init_state = False


    def setResultstate(self): 
        if self.result != "":
            self.result_state = True
        else:
            self.result_state = False


    def setErrorstate(self):
        if self.result == "계산할 수 없는 수식입니다.":
            self.error_state = True
        else:
            self.error_state = False
    
    
    def setOperstate(self):
        last = self.input[-1]
        if self.init_state or last in self.op+"(" or self.error_state == True:
            self.oper_state = False
        else:
            self.oper_state = True


    def setEqstate(self):
        if self.init_state or self.result_state or self.error_state:
            self.eq_state = False
        elif self.input[-1] in self.op:
            self.eq_state = False
        elif self.input[-1] == "." and self.input[-2] in self.op:
            self.eq_state = False
        else:
            self.eq_state = True
        
        
        
        # if self.init_state == False:
        #     if self.result_state == False:
        #         if self.error_state == False:
        #             self.eq_state = True
        #         else:
        #             self.eq_state = False
        #     else:
        #       self.eq_state = False  
        # else: 
        #     self.eq_state = False

        # if self.input[-1] == "." and self.input[-2] in self.op:
        #     self.eq_state = False


    def setParstate(self):
        if self.input[-1] == "." and self.input[-2] in self.op:
            self.par_state["open"] = False
            self.par_state["close"] = False
        else:
            self.par_state["open"] = True

            if len(self.parStack) > 0 and self.input[-1] not in self.op:
                self.par_state["close"] = True
            else:
                self.par_state["close"] = False   
        

    def setPointstate(self):
        if self.error_state:
            self.point_state = True
        else:
            for i in self.input[::-1]:                         # 수식을 역순으로 탐색
                if i == ".":                                   # 소수점이 이미 있으면 point_state = False
                    self.point_state = False
                    return
                else:
                    self.point_state = True
                if i in self.op:                               # 연산자를 만나면 조기 종료
                    return
        
    
    def setZerostate(self):
        if self.init_state or (self.input[-1] == "0" and self.input[-2] in self.op):
            self.zero_state = True
        else:
            self.zero_state = False
        

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
        
        if self.result_state == True:                       # 결과가 계산된 경우 
            self.text_history.append("")                    # 숫자 버튼을 눌렀을 때 이전 수식 & 결과를 히르토리 창에 출력
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
            self.result = ""                                # 결과 값 초기화
            self.input = new_digit
        
        elif self.zero_state:                               # 수식이 초기 상태이거나 마지막 숫자가 0으로 시작하는 경우
            self.input = self.input[:-1]
            self.input += new_digit
        
        elif self.input[-1] == ")":                         # 수식이 ")"로 끝나는 경우
            self.input += ("x" + new_digit)                 # 수식에 "x digit" 추가

        else:
            self.input += new_digit
    


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

    

    def openPar_Clicked(self):
        self.parStack.append("(")                           # 괄호 스택에 push
        if self.result_state:
            self.text_history.append("")                    # 히스토리창에 이전 수식 & 결과 출력
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
            self.result = ""
            self.input = "("
        else:
            if self.zero_state:                             # 마지막 숫자가 0으로 시작하는 경우
                self.input = self.input[:-1]                # 0을 지우고 열린 괄호 추가
                self.input += "("
            elif self.input[-1] in ".)123456789":           # 소수점, 닫힌 괄호, 숫자로 끝나는 경우
                self.input += "x("                          # 열린 괄호 앞에 "*"를 추가
            else:
                self.input += "("
      
        # if self.zero_state:                                     # 마지막 숫자가 0으로 시작하는 경우
        #     self.input = self.input[:-1]                        # 0을 지우고 열린 괄호 추가
        #     self.input += "("
        
        # elif self.input[-1] in ".)123456789":                   # 소수점, 닫힌 괄호, 숫자로 끝나는 경우
        #     if self.result:                                     # 수식이 이전 수식의 결과값인 경우
        #         self.text_history.append("")                    # 히스토리창에 이전 수식 & 결과 출력
        #         self.text_history.append(self.prev_input)
        #         self.text_history.append(self.result)
        #         self.result = ""
        #         self.input = "("                                # 결과값 초기화 & 수식을 열린 괄호로 초기화
        #     else:
        #         self.input += "*("                              # 열린 괄호 앞에 "*"를 추가
        
        # else:
        #     self.input += "("
            
    

    def closePar_Clicked(self):
        self.parStack.pop()                                     # 괄호 스택에서 원소 pop
        if self.input[-1] == "(":                               # 수식 마지막이 열린 괄호인 경우 0을 추가하고 닫는다.
            self.input += "0)"
        else:
            self.input += ")"

    
    def equal_Clicked(self):
        while len(self.parStack) > 0:                           # 닫힌 괄호 자동 완성
            if self.input[-1] == "(":
                self.input += "0)"
            else:
                self.input += ")"
            self.parStack.pop()
        
        try:
            res = eval(self.input.replace("x", "*"))
            
            if res == int(res):                                 # 소수점 이하가 0이면 정수로 출력
                self.result = str(int(res))
            else:
                self.result = str(res)
            
            self.error_state = False
        
        except:
            self.result = "계산할 수 없는 수식입니다."
        
        self.prev_input = self.input
        self.parStack = []

        if self.error_state == False:
            self.input = self.result
    

    def point_Clicked(self):
        if self.result_state == True:
            self.text_history.append("")
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
            self.result = ""
            self.input = "0."
        else:
            self.input += "."
    

    def ac_Clicked(self):
        if self.result_state:
            self.text_history.append("")
            self.text_history.append(self.prev_input)
            self.text_history.append(self.result)
        self.input = "0"
        self.result = ""
        self.parStack = []
    
    
    def undo_Clicked(self):
        if self.input[-1] == ")":                               # 괄호 삭제하는 경우
                self.parStack.append("(")
        elif self.input[-1] == "(":
            self.parStack.pop()

        if len(self.input) > 1:
            self.input = self.input[:-1]
        else:
            self.input = "0"
