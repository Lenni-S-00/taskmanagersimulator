# A file and a class for stylesheets
# Nothing special here

class Styles:
    tasks = """
            QLabel{
            color: #334E68;
            font-weight: 600;
            font-size: 14px;
            background: #EEFFFF;
            border: 1px solid #E2E8F0;
            }
            """
    taskinfo = """
            QLabel{
            color: #1C1C1C;
            font-weight: 600;
            font-size: 14px;
            background: #EEFFFF;
            border: 1px solid #E2E8F0;
            }
            """
    ready = """
            QLabel{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #91FF73;
                border: 1px solid #E2E8F0;
                }
            """
    cancelled = """
            QLabel{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #FF8888;
                border: 1px solid #E2E8F0;
                }
            """
    running = """
            QLabel{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #E0FF90;
                border: 1px solid #E2E8F0;
                }
            """
    paused = """
            QLabel{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #FFEA63;
                border: 1px solid #E2E8F0;
                }
            """
    queued = """
            QLabel{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #FEF7FF;
                border: 1px solid #E2E8F0;
                }
            """
    eta = """
            QLabel{
                color: #1C1C1C;
                font-weight: 600;
                font-size: 13px;
                background: #D1FFD1;
                border: 1px solid #E2E8F0;
                }
            """
    info = """
            QLabel{
                color: #1C1C1C;
                font-weight: 600;
                font-size: 13px;
                }
            """
    exit = """
            QPushButton{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #FF8F8F;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
                }
                QPushButton:hover{
                background: #FFE0E0;

                }
            """
    clearlog = """
            QPushButton{
                color: #334E68;
                font-weight: 600;
                font-size: 13px;
                background: #FFCA9E;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
                }
                QPushButton:hover{
                background: #FFD8B8;

                }
            """
    addtask = """
            QPushButton{
                color: #1C1C1C;
                font-weight: 600;
                font-size: 13px;
                background: #E0FF90;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
                }
                QPushButton:hover{
                background: #EBFFAD;

                }
            """
    taskresume = """
            QPushButton{
                color: #334E68;
                background: #BEFF66;
                border: 1px solid #E2E8F0;
                }
                QPushButton:hover{
                background: #CBFF87;

                }
            """
    taskpause = """
            QPushButton{
                color: #334E68;
                background: #FFEA63;
                border: 1px solid #E2E8F0;
                }
                QPushButton:hover{
                background: #FFFD8C;

                }
            """
    taskcancel = """
            QPushButton{
                color: #334E68;
                background: #FFB09E;
                border: 1px solid #E2E8F0;
                }
                QPushButton:hover{
                background: #FFC1B3;

                }
            """
    taskdelete = """
            QPushButton{
                color: #334E68;
                background: #FF734F;
                border: 1px solid #E2E8F0;
                }
                QPushButton:hover{
                background: #FF9B82;

                }
            """