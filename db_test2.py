import pymysql
import os
import subprocess

conn = pymysql.connect(
    host='여기에 DB 서버 IP 주소 입력',
    user='계정 아이디',       
    password='비밀번호',
    database='testdb',  # 연결할 DB (없어도 무관)
)

# 화면 지우기 기능을 'clear_screen'이라는 이름으로 미리 세팅해 둡니다.
def clear_screen():
    if os.name == 'nt':     # 만약 지금 쓰는 컴퓨터가 윈도우(nt)라면
        os.system('cls')    # cls 명령어를 실행
    else:                   # 윈도우가 아니라면 (맥, 리눅스 등)
        os.system('clear')

try:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                game_name VARCHAR(50)
            )
        """)
    conn.commit()
    while True:
        print("\n좋아하는 게임 종류 설문조사")
        print("1. 설문 참여하기")
        print("2. 설문 현황 확인하기")
        print('3. 나가기')
        print()
        a = input("선택: ")
        clear_screen()
        if a == "1":
            print("\n좋아하는 게임을 선택하세요")
            print()
            print("1. 리그오브레전드")
            print("2. 메이플스토리")
            print("3. 던전앤파이터")
            print("4. 배틀그라운드")
            print('5. 직접입력: ')
            b = input("\n선택: ")
                
            select_game = ""
            if b == "1":
                select_game='리그오브레전드'
            elif b == "2":
                select_game="메이플스토리"
            elif b == "3":
                select_game="던전앤파이터"
            elif b == "4":
                select_game="배틀그라운드"
            elif b == "5":
                select_game=input("게임 이름을 입력해주세요: ")
            else:
                print("다시 입력해주세요")
                continue
            print()
            with conn.cursor() as cur:
                insert_sql = "INSERT INTO votes (game_name) VALUES (%s)"
                cur.execute(insert_sql, (select_game,))
            
            conn.commit() 
            print(f"\n{select_game}에 투표가 완료되었습니다!\n")
            input("다음으로 이동하시려면 엔터를 누르세요.")
            clear_screen()
        elif a == '2':
            print("\n[ 현재 설문 현황 ]\n")
            
            with conn.cursor() as cur:
                select_sql = "SELECT game_name, COUNT(*) FROM votes GROUP BY game_name"
                cur.execute(select_sql)
                results = cur.fetchall() 
            
            if not results:
                print("아직 참여한 데이터가 없습니다.")
            else:
                total_votes = sum(row[1] for row in results)
                print(f"** 총 참여자 수: {total_votes}명 **\n")

                
                for row in results:
                    game_name = row[0]   # 게임 이름
                    vote_count = row[1]  # 득표 수
                    
                    percentage = (vote_count / total_votes) * 100
                    
                    print(f"{game_name} ===> {vote_count}표 ({percentage:.1f}%)")
                input("다음으로 이동하시려면 엔터를 누르세요.")
                clear_screen()
       

        elif a == '3':
            print("설문조사 프로그램을 종료합니다.")
            break 

        else:
            print("⚠️ 잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")

except pymysql.MySQLError as e:
    print("DB 연결 또는 실행 오류:", e)

finally:
    if conn:
        conn.close()
        print("✅ DB 접속 정상 종료")