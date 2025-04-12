import os
import time

# 테스트용 디렉토리 구조 만들기
os.makedirs('testdir/testdir1', exist_ok=True)
os.makedirs('testdir/testdir2', exist_ok=True)
os.makedirs('testdir/testdir3', exist_ok=True)

# 텍스트 파일 생성
file_contents = {
    'dog1.txt': 'This is dog1 file',
    'dog2.txt': '',
    'doog1.txt': '',
    'doooog1.txt': '',
    'test1.txt': '',
    'test2.txt': '',
    'test3.txt': '',
    'test4.jpg': '',
    'test5.jpg': ''
}

for filename, content in file_contents.items():
    with open(f'testdir/{filename}', 'w') as f:
        f.write(content)

# 수정 시간 조정 (도움말에서 사용된 newer 테스트를 위해)
# dog2.txt 를 가장 오래된 파일로 만들고, dog1.txt는 최신 파일로 설정
old_time = time.time() - 3 * 24 * 60 * 60  # 3일 전
new_time = time.time() - 1 * 24 * 60 * 60  # 1일 전

os.utime('testdir/dog2.txt', (old_time, old_time))
os.utime('testdir/dog1.txt', (new_time, new_time))

print("✅ 테스트 환경이 'testdir' 폴더에 생성되었습니다.")