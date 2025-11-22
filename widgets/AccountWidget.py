from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton, QMessageBox, QLabel, QSpinBox, QHBoxLayout, \
    QCheckBox
from utils.PostgreSQLManager import PostSQLManager
from utils.DataManager import DataManager
from functools import partial

class RegisterWidget(QWidget):
    '''
    회원가입 창을 띄웁니다.
    '''
    pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.name_lb = QLabel("회원가입")

        self.user_id_lb = QLabel("ID")
        self.user_id_le = QLineEdit()

        self.password_lb = QLabel("PW")
        self.password_le = QLineEdit()
        self.password_show_chb = QCheckBox()

        self.password_confirm_lb= QLabel("PW confirm")
        self.password_confirm_le = QLineEdit()
        self.password_confirm_show_chb = QCheckBox()

        self.admission_year_lb = QLabel("입학년도")
        self.admission_year_le = QLineEdit()

        self.rest_semester_count_lb = QLabel("휴학 기간")
        self.rest_semester_count_sp = QSpinBox()

        self.college_lb = QLabel("소속 대학")
        self.college_le = QLineEdit()

        self.department_lb = QLabel("소속 학부")
        self.department_le = QLineEdit()

        self.major_lb = QLabel("소속 학과")
        self.major_le = QLineEdit()

        self.login_btn = QPushButton('로그인')
        self.register_btn = QPushButton("회원가입")

        def change_echo_state(pw_le:QLineEdit, chb:QCheckBox):
            if chb.isChecked():
                pw_le.setEchoMode(QLineEdit.Normal)
            else:
                pw_le.setEchoMode(QLineEdit.Password)

        self.password_le.setEchoMode(QLineEdit.Password)
        self.password_confirm_le.setEchoMode(QLineEdit.Password)
        self.register_btn.pressed.connect(self.regist)
        self.login_btn.pressed.connect(self.pressed.emit)
        self.password_confirm_show_chb.released.connect(
            partial(change_echo_state, self.password_confirm_le, self.password_confirm_show_chb))
        self.password_show_chb.released.connect(
            partial(change_echo_state, self.password_le, self.password_show_chb))

        vbox = QVBoxLayout()

        vbox.addWidget(self.name_lb)

        id_hbox = QHBoxLayout()
        id_hbox.addWidget(self.user_id_lb)
        id_hbox.addWidget(self.user_id_le)
        vbox.addLayout(id_hbox)

        pw_hbox = QHBoxLayout()
        pw_hbox.addWidget(self.password_lb)
        pw_hbox.addWidget(self.password_le)
        pw_hbox.addWidget(self.password_show_chb)
        vbox.addLayout(pw_hbox)

        pwc_hbox = QHBoxLayout()
        pwc_hbox.addWidget(self.password_confirm_lb)
        pwc_hbox.addWidget(self.password_confirm_le)
        pwc_hbox.addWidget(self.password_confirm_show_chb)
        vbox.addLayout(pwc_hbox)

        ay_hbox = QHBoxLayout()
        ay_hbox.addWidget(self.admission_year_lb)
        ay_hbox.addWidget(self.admission_year_le)
        vbox.addLayout(ay_hbox)

        rsc_hbox = QHBoxLayout()
        rsc_hbox.addWidget(self.rest_semester_count_lb)
        rsc_hbox.addWidget(self.rest_semester_count_sp)
        vbox.addLayout(rsc_hbox)

        college_hbox = QHBoxLayout()
        college_hbox.addWidget(self.college_lb)
        college_hbox.addWidget(self.college_le)
        vbox.addLayout(college_hbox)

        department_hbox =QHBoxLayout()
        department_hbox.addWidget(self.department_lb)
        department_hbox.addWidget(self.department_le)
        vbox.addLayout(department_hbox)

        major_hbox = QHBoxLayout()
        major_hbox.addWidget(self.major_lb)
        major_hbox.addWidget(self.major_le)
        vbox.addLayout(major_hbox)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.login_btn)
        btn_hbox.addWidget(self.register_btn)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

    def regist(self):
        user_id = self.user_id_le.text()
        if PostSQLManager.check_student_id(user_id):
            return
        else:
            # 에러 방지용으로 str 값들 확인하는 함수 만들 것
            password = self.password_le.text()
            password_c = self.password_confirm_le.text()
            if password != password_c:
                message_box = QMessageBox.warning(self, "경고", "비밀번호가 일치하지 않습니다.")
                return
            salt = DataManager.get_salt()
            admission_year = self.admission_year_le.text()
            rest_semester_count = self.rest_semester_count_sp.value()
            college = self.college_le.text()
            department = self.department_le.text()
            major = self.major_le.text()
            if DataManager.check_year_str(admission_year):
                hashed_pw = DataManager.hash_pw(password,salt)
                PostSQLManager.add_account(
                    student_id=user_id,
                    hashed_password=hashed_pw,
                    salt=salt,
                    admission_year=admission_year,
                    rest_semester_count=rest_semester_count,
                    college = college,
                    department=department,
                    major=major
                )
                self.pressed.emit()
            else:
                pass

class LoginWidget(QWidget):
    '''
    로그인 창을 띄웁니다.
    '''
    pressed = pyqtSignal()
    logined = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.auto_login_chb = QCheckBox("자동 로그인")

        self.name_lb = QLabel("로그인")

        self.student_id_lb = QLabel("ID : ")
        self.student_id_le = QLineEdit()
        self.password_lb = QLabel("PW : ")
        self.password_le = QLineEdit()
        self.login_btn = QPushButton("로그인")
        self.register_btn = QPushButton("회원가입")

        self.password_le.setEchoMode(QLineEdit.Password)
        self.login_btn.pressed.connect(self.login)
        self.register_btn.pressed.connect(self.pressed.emit)
        self.password_le.returnPressed.connect(self.login)

        self.set_account()

        vbox = QVBoxLayout()

        name_hbox = QHBoxLayout()
        name_hbox.addWidget(self.name_lb)
        name_hbox.addWidget(self.auto_login_chb)
        vbox.addLayout(name_hbox)

        id_hbox = QHBoxLayout()
        id_hbox.addWidget(self.student_id_lb)
        id_hbox.addWidget(self.student_id_le)
        vbox.addLayout(id_hbox)

        pw_hbox = QHBoxLayout()
        pw_hbox.addWidget(self.password_lb)
        pw_hbox.addWidget(self.password_le)
        vbox.addLayout(pw_hbox)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.login_btn)
        btn_hbox.addWidget(self.register_btn)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

    def set_account(self):
        if DataManager.has_account():
            account_dict:dict[str,str] = DataManager.load_account()
            self.student_id_le.setText(account_dict["id"])
            self.password_le.setText(account_dict["pw"])
            self.auto_login_chb.setCheckState(2)

    def login(self):
        user_id = self.student_id_le.text()
        password = self.password_le.text()

        if PostSQLManager.check_student_id(user_id):
            salt = PostSQLManager.get_salt(user_id)
            hashed_pw = DataManager.hash_pw(password, salt)
            account_data = PostSQLManager.get_student_account(user_id, hashed_pw)
            if account_data is not None:
                account = DataManager.datas2student(account_data)
                DataManager.login(account)
                if self.auto_login_chb.isChecked():
                    DataManager.save_account(user_id, password)
                self.logined.emit()
            else:
                QMessageBox.warning(self, "경고", "사용자의 ID가 일치하지 않습니다..")
        else:
            QMessageBox.warning(self, "경고", "사용자의 ID가 존재하지 않습니다.")

    def closeEvent(self, a0):
        if not self.auto_login_chb.isChecked():
            DataManager.del_account()
        a0.accept()

class AccountWidget(QWidget):
    '''
    로그인과 회원가입 창을 관리합니다.
    '''
    logined = pyqtSignal()
    adjust = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.login_wg = LoginWidget()
        self.register_wg = RegisterWidget()

        self.login_wg.pressed.connect(self.set_register)
        self.register_wg.pressed.connect(self.set_login)
        self.login_wg.logined.connect(self.logined.emit)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.login_wg)

        self.setLayout(self.vbox)

    def set_login(self):
        self.vbox.removeWidget(self.register_wg)
        self.register_wg.close()
        self.vbox.addWidget(self.login_wg)
        self.login_wg.show()
        self.adjust.emit()

    def set_register(self):
        self.vbox.removeWidget(self.login_wg)
        self.login_wg.close()
        self.vbox.addWidget(self.register_wg)
        self.register_wg.show()
        self.adjust.emit()

    def show_schedule_widget(self):
        self.vbox.removeWidget(self.login_wg)
        self.login_wg.close()
        self.logined.emit()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)

    login_wg = AccountWidget()
    login_wg.show()

    sys.exit(app.exec_())
