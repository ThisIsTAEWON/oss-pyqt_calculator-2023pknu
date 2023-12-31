import sys
from PyQt5.QtWidgets import *
import re
import math

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout = QGridLayout()
        layout_equation_solution = QFormLayout()
        

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.equation = QLineEdit("")
        self.solution = QLineEdit("")
        self.operand = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(self.solution)
        self.button_C_clicked()

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_percentage = QPushButton("%")
        
        button_reciprocal = QPushButton("1/x")
        button_exp = QPushButton("x^2")
        button_sqrt = QPushButton("x^(1/2)")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_percentage.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        
        button_reciprocal.clicked.connect(lambda state, operation = "1/x": self.button_single_operation_clicked(operation))
        button_exp.clicked.connect(lambda state, operation = "x^2": self.button_single_operation_clicked(operation))
        button_sqrt.clicked.connect(lambda state, operation = "x^(1/2)": self.button_single_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout.addWidget(button_plus, 4, 4)
        layout.addWidget(button_minus, 3, 4)
        layout.addWidget(button_product, 2, 4)
        layout.addWidget(button_division, 1, 4)
        layout.addWidget(button_percentage, 0, 1)
        
        layout.addWidget(button_reciprocal, 1, 1)
        layout.addWidget(button_exp, 1, 2)
        layout.addWidget(button_sqrt, 1, 3)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_CE = QPushButton("CE")
        button_C = QPushButton("C")
        button_backspace = QPushButton("Backspace")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_CE.clicked.connect(self.button_CE_clicked)
        button_C.clicked.connect(self.button_C_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout.addWidget(button_CE, 0, 2)
        layout.addWidget(button_C, 0, 3)
        layout.addWidget(button_backspace, 0, 4)
        layout.addWidget(button_equal, 5, 4)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
        
        layout.addWidget(number_button_dict[0], 5, 2)
        layout.addWidget(number_button_dict[1], 4, 1)
        layout.addWidget(number_button_dict[2], 4, 2)
        layout.addWidget(number_button_dict[3], 4, 3)
        layout.addWidget(number_button_dict[4], 3, 1)
        layout.addWidget(number_button_dict[5], 3, 2)
        layout.addWidget(number_button_dict[6], 3, 3)
        layout.addWidget(number_button_dict[7], 2, 1)
        layout.addWidget(number_button_dict[8], 2, 2)
        layout.addWidget(number_button_dict[9], 2, 3)

        ### 소숫점 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout.addWidget(button_dot, 5, 3)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        operand = self.operand.text()
        if operand == "0":
            operand = ""
        operand += str(num)
        self.operand.setText(operand)
        self.solution.setText(operand)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        if equation == "0":
            equation = ""
        
        operand = self.operand.text()
        equation += operand
        solution = eval(equation)
        equation += operation
        self.operand.setText("0")
        self.equation.setText(equation)
        self.solution.setText(str(solution))

    def button_equal_clicked(self):
        equation = self.equation.text()
        if equation == "0":
            self.button_C_clicked()
            equation = ""
        equation += self.operand.text()
        solution = eval(equation)
        self.operand.setText("0")
        self.equation.setText("0")
        self.solution.setText(str(solution))
    
    def button_single_operation_clicked(self, operation):
        operand = self.operand.text()
        if operand == "0":
            self.solution.setText("0")
            return
        
        if operation == "1/x":
            operand = 1 / float(operand)
        elif operation == "x^2":
            operand = math.pow(float(operand), 2)
        elif operation == "x^(1/2)":
            operand = math.sqrt(float(operand))
        else:
            return
        
        self.operand.setText(str(operand))
        self.solution.setText(str(operand))

    def button_C_clicked(self):
        self.operand.setText("0")
        self.equation.setText("0")
        self.solution.setText("0")
        
    def button_CE_clicked(self):
        self.operand.setText("0")
        self.solution.setText("0")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        solution = self.solution.text()
        equation = equation[:-1]
        solution = solution[:-1]
        self.equation.setText(equation)
        self.solution.setText(solution)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())