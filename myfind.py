import os
import argparse
import datetime
import re


def find_files(start_path, **options):
    import time

    # 기준 파일의 수정 시간 가져오기 (newer 옵션용)
    newer_than_time = None
    if options.get('newer_than_file'):
        try:
            newer_than_time = os.path.getmtime(options['newer_than_file'])
        except (FileNotFoundError, PermissionError):
            print(f"Error: Cannot access reference file '{options['newer_than_file']}'")
            return

    # mtime 옵션 처리를 위한 현재 시간 가져오기
    current_time = time.time()
    
    # 디렉토리 순회를 위한 os.walk 사용
    for root, dirs, files in os.walk(start_path):
        # 모든 항목(파일+디렉토리)에 대해 반복
        all_items = [(name, os.path.join(root, name), 'f') for name in files]
        all_items.extend([(name, os.path.join(root, name), 'd') for name in dirs])
        
        for name, path, item_type in all_items:

            if name.startswith('.'): #숨겨진 파일 무시(.)으로 시작
                continue

            # 각 옵션에 따른 조건 확인
            match = True

            # -name
            if options.get('name') and match:
                if name != options['name']:
                    match = False

            # -type
            if options.get('type') and options['type'] != item_type:
                match = False
            
            # 아래 옵션들은 파일 속성에 접근해야 하므로 파일 정보 가져오기
            try:
                file_stat = os.stat(path)
            except (FileNotFoundError, PermissionError):
                continue
                
            # -newer
            if options.get('newer_than_file') and match and newer_than_time:
                if file_stat.st_mtime <= newer_than_time:
                    match = False
            
            #   size
            if options.get('size') and match:
                size_str = options['size']
                size_val = size_str[1:] if size_str[0] in ['+', '-'] else size_str
                try:
                    size_val = int(size_val)
                    file_size_blocks = file_stat.st_size/512 #512로 변환
                    
                    if size_str.startswith('+') and file_size_blocks <= size_val:
                        match = False
                    elif size_str.startswith('-') and file_size_blocks >= size_val:
                        match = False
                    elif not size_str.startswith('+') and not size_str.startswith('-') and file_size_blocks != size_val:
                        match = False
                except ValueError:
                    match = False
            
            # -perm
            if options.get('perm') and match:
                try:
                    # 8진수 문자열을 정수로 변환
                    requested_mode = int(options['perm'], 8)
                    # 파일 모드에서 하위 9비트(rwxrwxrwx)만 비교
                    actual_mode = file_stat.st_mode & 0o777
                    if actual_mode != requested_mode:
                        match = False
                except ValueError:
                    match = False
            
            # -mtime
            if options.get('mtime') and match:
                mtime_str = options['mtime']
                try:
                    # 첫 문자가 +나 -인지 확인
                    if mtime_str.startswith('+'):
                        days = int(mtime_str[1:])
                        comparison = '>' 
                    elif mtime_str.startswith('-'):
                        days = int(mtime_str[1:])
                        comparison = '<'
                    else:
                        days = int(mtime_str)
                        comparison = '=' 
                    
                    # 파일 수정 시간과 현재 시간의 차이를 일 단위로 변환
                    days_diff = (current_time - file_stat.st_mtime) / (24 * 3600)
                    
                    if comparison == '>' and days_diff <= days:
                        match = False
                    elif comparison == '<' and days_diff >= days:
                        match = False
                    elif comparison == '=' and (days_diff < days or days_diff >= days + 1):
                        match = False
                except ValueError:
                    match = False
            
            if match:
                relative_path = os.path.relpath(path, start_path)
                print('./' + relative_path.replace('\\', '/')) #출력되는 슬래시 방향이 달라 수정함


def main():
    parser = argparse.ArgumentParser(description='Python implementation of the find command')
    parser.add_argument('start_path', type=str, help='Starting directory path')
    parser.add_argument('-name', type=str, help='File name pattern to search for (regular expression supported)')
    parser.add_argument('-type', type=str, choices=['f', 'd'], help='File type (f for file, d for directory)')
    parser.add_argument('-newer', type=str, help='File to compare modification time against')
    parser.add_argument('-size', type=str, help='File size (+n for greater than n*512 bytes, -n for less than n*512 bytes, n for exactly n*512 bytes)')
    parser.add_argument('-perm', type=str, help='File permission (e.g., 644)')
    parser.add_argument('-mtime', type=str, help='File modification time (-n for within n days, +n for older than n days, n for exactly n days ago)')

    args = parser.parse_args()

    find_files(args.start_path, name=args.name, type=args.type, 
               newer_than_file=args.newer, size=args.size, perm=args.perm, mtime=args.mtime)

if __name__ == '__main__':
    main()