import requests  # HTTP 요청을 보내는 라이브러리. get 메소드를 사용해 웹 서버와 상호작용
import json   # JSON 형식의 데이터를 처리하는 데 사용
import pandas as pd   # pandas 라는 데이터 분석 라이브러리를 'pd'라는 이름으로 사용할 수 있게 불러옴. DataFrame이라는 2차원 테이블 형태의 데이터 구조 제공
from tkinter import *   # tkinter 라는 GUI 애플리케이션을 생성하는 라이브러리를 사용할 수 있게 불러옴.
from tkinter import messagebox # tkinter의 하위 모듈인 messagebox 를 현재 코드에서 사용할 수 있게 불러옴. 알림 메시지 표시 또는 의사를 묻는 대화 상자 생성
from datetime import datetime  # 파이썬의 표준 라이브러리인 'datetime'에서 'datetime' 클래스를 현재 코드에서 사용할 수 있게 불러옴


# OpenWeatherMap API 키
key = 'd9fe7788fdc23604dc20352b06456e57'


def get_weather_data(city, key):
    try:
        # 웹 페이지에 get 요청 보냄, 입력받은 도시의 위도와 경도 정보 불러오기 
        location = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={key}")
        location = json.loads(location.text)   # 서버로부터 받은 응답을 .text 를 통해 확인, JSON 문자열을 파이썬의 딕셔너리로 변환하는 json.loads() 함수 사용
        lat = location[0]['lat']  # 위도 정보 추출
        lon = location[0]['lon']  # 경도 정보 추출  

        # 위도와 경도를 사용하여 OpenWeatherMap의 날씨 예보 API에 GET 요청 보냄  
        api = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={key}"
        result = requests.get(api)   # 웹 페이지에 get 요청 보냄
        result = json.loads(result.text)    # 서버로부터 받은 응답을 .text 를 통해 확인, JSON 문자열을 파이썬의 딕셔너리로 변환하는 json.loads() 함수 사용
        
        weather = list()  # 날씨 예보 저장하는 리스트 생성
        # 각 예보 데이터에 대해 필요한 정보를 추출하여 리스트에 추가
        for i in range(result['cnt']):
            ith = [result['list'][i]['dt_txt'],
                   result['list'][i]['main']['temp'],
                   result['list'][i]['main']['temp_min'],
                   result['list'][i]['main']['temp_max'],
                   result['list'][i]['main']['humidity'],
                   # 강수량 정보 없으면 0으로 처리
                   result['list'][i]['rain']['3h'] if 'rain' in result['list'][i] and '3h' in result['list'][i]['rain'] else 0]
            weather.append(ith)

        # 리스트를 데이터프레임으로 변환 
        weather_df = pd.DataFrame(weather, columns=['datetime', 'temp', 'temp_min', 'temp_max', 'humidity', 'rain'])

        return weather_df
    
    # 예외 처리
    except Exception as e:   # try 블록에서 발생하는 모든 예외를 처리하겠다는 의미, 발생한 예외 객체를 e라는 이름의 변수로 참조하겠다는 의미
        print(f"An error occurred: {e}")   # 발생한 예외 객체를 문자열로 변환하여 출력 
        return None


def update_weather():
    city = city_entry.get()   # 사용자가 입력한 도시 이름 가져오기 
    # 도시 이름이 입력되지 않은 경우, 오류 메시지를 표시하고 함수 종료
    if not city:
        # messagebox.showerror(): 오류 메시지를 표시하는 대화 상자 생성, 사용자에게 오류가 발생했음을 알릴 때 사용
        messagebox.showerror("Error", "Please enter a city")
        return

    # 오늘 날짜에 해당하는 기상 정보들(3시간 단위) 출력
    weather_df = get_weather_data(city, key)
    if weather_df is not None:
        today = datetime.now().strftime('%Y-%m-%d')   # 현재 날짜를 'YYYY-MM-DD' 형식의 문자열로 변환
        today_weather = weather_df[weather_df['datetime'].str.contains(today)]
        # 오늘 날짜에 해당하는 기상 정보가 있는 경우
        if not today_weather.empty:
            # 기존의 기상 정보 삭제
            weather_text.delete(1.0, END)   # END: Listbox의 마지막 위치를 가리킴(Tkinter의 Listbox 위젯에서 항목을 추가하거나 삭제할 때 위치를 지정하는데 사용)
            weather_text.insert(END, today_weather.to_string(index=False))   # 새로운 기상 정보를 텍스트 박스에 입력
        else:
            # 오늘 날짜에 해당하는 기상 정보가 없는 경우
            # messagebox.showinfo(): 정보를 제공하는 메시지를 표시하는 대화 상자 생성, 일반적 정보 제공할 때 사용
            messagebox.showinfo("Info", "No weather data available for today")

# 기본 창 생성
root = Tk()  # tkinter 객체 생성 
root.title("Weather and To-do App")  # 창의 제목 설정
root.geometry("500x550")  # 창의 크기 설정

# 날씨 부분에 대한 프레임 생성, 기본 창에 추가  
weather_frame = Frame(root)   # 다른 위젯들을 그룹화하거나 구조화하는 데 사용되는 컨테이너, 하나의 위젯처럼 배치하거나 조작 가능
weather_frame.pack()

# 도시 이름을 입력받는 레이블 생성, 날씨 프레임에 추가
city_label = Label(weather_frame, text="Enter a city (in English):")
city_label.pack()

# 도시 이름을 입력받는 텍스트 엔트리 생성, 날씨 프레임에 추가
city_entry = Entry(weather_frame)  # Entry(): Tkinter GUI 라이브러리에서 제공하는 위젯, 사용자로부터 한 줄의 텍스트 입력을 받는 데 사용
city_entry.pack()

# 날씨 정보를 업데이트하는 버튼 생성, 날씨 프레임에 추가, 버튼 클릭 시 update_weather 함수 호출
update_button = Button(weather_frame, text="Update Weather", command=update_weather)
update_button.pack()

# 날씨 정보를 표시할 텍스트 박스 생성, 날씨 프레임에 추가
weather_text = Text(weather_frame, height = 10)    # Text(): 여러 줄의 텍스트 입력을 받는 데 사용, width(너비)/height(높이) 설정 가능 
weather_text.pack()


# 할 일 목록에 대한 프레임 생성, 기본 창에 추가
todo_frame = Frame(root)
todo_frame.pack()

tasks = []   # 할 일 목록 저장 리스트 생성
completed_tasks = []   # 완료된 할 일 목록 저장 리스트 생성

# 할 일을 입력받는 레이블 생성, 할 일 프레임에 추가
task_label = Label(todo_frame, text="할 일:")
task_label.pack()

# 할 일을 입력받는 텍스트 엔트리 생성, 할 일 프레임에 추가
task_var = StringVar()   # StringVar(): Tkinter 라이브러리에서 제공하는 클래스 
task_entry = Entry(todo_frame, textvariable=task_var)   # textvariable 옵션: StringVar() 변수(여기서는 task_var)와 텍스트 엔트리 위젯을 연결하여 위젯의 값이 변경될 때마다 변수의 값도 자동으로 업데이트
task_entry.pack()

# 마감일을 입력받는 레이블 생성, 할 일 프레임에 추가
deadline_label = Label(todo_frame, text="마감일:")
deadline_label.pack()

# 마감일을 입력받는 텍스트 엔트리 생성, 할 일 프레임에 추가
deadline_var = StringVar()
deadline_entry = Entry(todo_frame, textvariable=deadline_var)
deadline_entry.pack()

# 할 일 목록을 표시할 리스트 박스 생성, 할 일 프레임에 추가
task_listbox = Listbox(todo_frame, width=50)   # Listbox(): 여러 개의 선택지를 제시하고 그 중 하나 이상을 선택하도록 함, 여러 개의 항목 추가 가능 
task_listbox.pack()


def add_task():
    # 사용자로부터 입력 받은 할 일, 마감일 정보를 가져옴
    task = task_var.get()
    deadline = deadline_var.get()

    # 할 일이 입력되지 않았으면 에러 메시지를 표시하고 함수를 종료
    if not task.strip():   # strip(): 공백 문자 제거
        messagebox.showerror("오류", "할 일을 입력해주세요.")
        return

    # 날짜 형식 검증
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("오류", "날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요.")
        return

    # 할 일, 마감일, 그리고 할 일의 색상을 튜플로 묶어 리스트에 추가
    tasks.append((task, deadline, "black"))

    # 리스트를 마감일 순서로 정렬, datetime.strptime() 함수를 사용하여 문자열 형태의 마감일을 datetime 객체로 변환하여 비교
    # key 파라미터: 정렬 기준 설정 
    tasks.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"))  # tasks 리스트의 각 요소에서 두 번째 값(x[1])을 날짜로 해석하고, 그 날짜를 기준으로 tasks를 정렬

    # 할 일과 마감일을 입력받는 Entry 위젯의 내용 지우기(창 닫기 전까지 계속 입력받기 위해) 
    task_var.set("")   # set() 함수는 Entry 위젯의 내용 설정
    deadline_var.set("")

    # Listbox 업데이트
    update_listbox()


def update_listbox():
    # Listbox 위젯의 모든 항목 제거 
    task_listbox.delete(0, END)   # delete() 함수는 Listbox의 특정 범위의 항목을 제거함

    # 정렬된 리스트를 Listbox 위젯에 추가
    # tasks라는 리스트를 순회하면서 각 요소(task)와 그 요소의 인덱스(i)를 얻음 
    for i, task in enumerate(tasks):    # enumerate(): 순회 가능한 객체(리스트, 튜플, 문자열 등)를 입력으로 받아 인덱스와 그에 해당하는 값을 튜플 형태로 반환
        # 할 일과 마감일을 합쳐서 하나의 문자열로 만들기
        task_text = f"{task[0]} - ({task[1][5:]})"
        # 만들어진 문자열을 Listbox 위젯에 추가
        task_listbox.insert(i, task_text)   # insert() 함수는 Listbox의 특정 위치에 항목을 추가
        # Listbox의 항목 색상 설정
        task_listbox.itemconfig(i, {"fg": task[2]})   # itemconfig() 함수는 Listbox의 특정 항목의 설정을 변경

    # 완료한 항목들도 목록에 추가
    for i, task in enumerate(completed_tasks, start=len(tasks)):
        # 완료한 항목도 마찬가지로 할 일과 마감일을 합쳐서 하나의 문자열로 만들기 
        task_text = f"{task[0]} - ({task[1][5:]})"
        # 만들어진 문자열을 Listbox 위젯에 추가
        task_listbox.insert(i, task_text)
        # Listbox의 항목 색상 설정
        task_listbox.itemconfig(i, {"fg": task[2]})

        
def complete_task():
    # Listbox에서 현재 선택된 항목의 인덱스를 가져옴
    sel = task_listbox.curselection()   # curselection(): 사용자가 현재 선택한 항목의 인덱스 반환 

    # 선택된 항목이 없으면 함수를 종료
    if not sel:
        return

    # 선택된 항목의 인덱스와 내용을 가져옴
    idx = sel[0]
    task = tasks.pop(idx)  # 해당 인덱스의 할 일을 tasks 리스트에서 제거

    # 완료된 항목의 글자색을 변경
    completed_task = (task[0], task[1], "lightgray")

    # 완료된 항목을 완료된 할 일 리스트에 추가
    completed_tasks.append(completed_task)

    # Listbox 최신 상태로 업데이트
    update_listbox()

    # Listbox에서 모든 항목의 선택을 해제
    task_listbox.selection_clear(0, END)

    
def cancel_task():
    # 현재 선택된 항목의 인덱스를 가져옴
    sel = task_listbox.curselection()

    # 선택된 항목이 없거나 완료되지 않은 항목이면 함수를 종료
    if not sel or sel[0] < len(tasks):
        return

    # 선택된 항목의 인덱스와 내용을 가져옴
    idx = sel[0] - len(tasks)
    task = completed_tasks.pop(idx)   # 해당 인덱스의 할 일을 completed_tasks 리스트에서 제거 

    # 완료 취소된 항목의 글자색을 변경, 다시 할 일로 표시 
    canceled_task = (task[0], task[1], "black")

    # 완료 취소된 항목을 다시 리스트의 적절한 위치에 삽입
    tasks.append(canceled_task)
    tasks.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"))

    # Listbox 최신 상태로 업데이트
    update_listbox()

    # Listbox에서 모든 항목의 선택을 해제
    task_listbox.selection_clear(0, END)
    
def on_select(event):
    # 현재 선택된 항목의 인덱스를 가져옴
    sel = task_listbox.curselection()

    # 선택된 항목이 있고, 그게 완료된 항목이면 완료 취소 버튼 활성화
    if sel and sel[0] >= len(tasks): 
        cancel_button.config(state=NORMAL)   # NORMAL: Tkinter의 위젯 상태를 나타내는 상수, 위젯이 정상적으로 동작하고 사용자의 입력을 받을 수 있는 상태
    # 그 외의 경우에는 완료 취소 버튼 비활성화
    else:
        cancel_button.config(state=DISABLED)  # DISABLED: Tkinter의 위젯 상태를 나타내는 상수,위젯이 비활성화되어 사용자의 입력을 받지 않는 상태

#할 일을 추가하는 버튼 생성, 버튼 클릭 시 add_task 함수 호출
add_button = Button(root, text="할 일 추가", command=add_task)
add_button.pack()

#할 일을 완료하는 버튼 생성, 버튼 클릭 시 complete_task 함수 호출
complete_button = Button(root, text="완료", command=complete_task)
complete_button.pack()

#할 일을 완료 취소하는 버튼 생성, 버튼 클릭 시 cansel_task 함수 호출 
cancel_button = Button(root, text="완료 취소", command=cancel_task, state=DISABLED)
cancel_button.pack()

#Listbox 항목 선택 시 완료 취소 버튼 활성화/비활성화
task_listbox.bind("<<ListboxSelect>>", on_select)  # task_listbox에서 항목을 선택하면 on_select 함수가 호출되도록 설정

root.mainloop()
