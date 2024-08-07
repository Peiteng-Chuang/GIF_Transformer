import time,os,cv2
from PIL import Image

class GTA(object):

    def __init__(self,
                 gif_path='./gif_to_transform/target.gif',          #GIF檔案的路徑，我將目標設為target.gif
                 save_path='./gif_frame/',                          #GIF切片後的圖片存放路徑
                 file_name = './frame_txt/thebigtxt.txt',           #寫入的巨大txt文本路徑
                 WIDTH = 120,                                       #設定輸出圖像寬度
                 HEIGHT = 37,                                       #設定輸出圖像高度
                 ascii_char = "$$$$@@@@####****              "      # rickroll專用
                 ):
        # 指定GIF 文件路徑
        self.gif_path = gif_path
        self.save_path=save_path
        self.gif = Image.open(gif_path)
        self.frame_count = self._count_frames()

        self.file_name = file_name
        self.WIDTH = WIDTH # 寬
        self.HEIGHT = HEIGHT # 高
        self.lines_to_read = self.HEIGHT
        #self.ascii_char ="   ._\"^\:=,;><~+=?][1  "        # 無牙龍專用
        self.ascii_char = ascii_char 


    def _count_frames(self):
        frame_count = 0
        while True:
            try:
                self.gif.seek(frame_count)
                frame_count += 1
            except EOFError:
                break
        self.gif.seek(0)  # 回到 GIF 文件的第一幀
        return frame_count


    def clear_screen(self):
        if os.name == 'posix':  # Unix/Linux/MacOS
            os.system('clear')
        elif os.name == 'nt':  # Windows
            os.system('cls')


    def dancing(self):
        while True:

            last_position = 0
            with open(self.file_name, 'r') as file:
                while True:
                    lines = []
                    file.seek(last_position)
                    for _ in range(self.lines_to_read):
                        line = file.readline() 
                        if not line:
                            break  
                        lines.append(line.rstrip())
                    next_position = file.tell()
                    data=lines

                    if not data:
                        break
                    for line in data:
                        print(line)
                    last_position = next_position
                    time.sleep(0.035)
                    self.clear_screen()
            file.close()


    def files_in_directory(self,directory):
        try:
            files = os.listdir(directory)
            files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
            return files
        except:
            print("檔案不存在")
            return 0


    def count_files_in_directory(self,directory):
        try:
            files = os.listdir(directory)
            files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
            file_count = len(files)
            return file_count
        except:
            print("檔案不存在")
            return 0


    def get_char(self,gray_value):
    
        length = len(self.ascii_char) # 根據傳進來的灰階值判斷此位置要使用哪個字元
        unit = 256.0 / length # 區分灰階範圍
        return self.ascii_char[int(gray_value / unit)]

    def transform_imgtotxt(self):       #將圖片轉成ASCII符號加入txt
        filepath=self.file_name
        if os.path.exists(filepath):
                os.remove(filepath)
        file_len=self.count_files_in_directory("./gif_frame")
        print(f"transform {file_len} images into txt...")
        for a1 in range(file_len) :
            frame_name='.//gif_frame//frame_'+ str(a1) +'.png'
            img = cv2.imread(frame_name, cv2.IMREAD_GRAYSCALE) # 將圖片自動轉為灰階圖片
            img = cv2.resize(img, (self.WIDTH, self.HEIGHT)) # 將灰階圖縮小成指定大小
            txt = ""
            for i in range(self.HEIGHT):
                for j in range(self.WIDTH):
                    txt += self.get_char(img[i][j]) # 轉為指定字符
                txt += '\n'
            with open(filepath, 'a') as file:
                file.write(txt)

    def clear_save_path(self):
        if os.path.exists(self.save_path):
            files = os.listdir(self.save_path)
            for f in files:
                os.remove(os.path.join(self.save_path, f))
                print(f"舊資料 '{self.save_path}{f}' 已成功删除。")
        else:
            os.makedirs(self.save_path)
            print(f"新目錄 '{self.save_path}' 已成功創建。")

    def save_frames(self):
        self.clear_save_path()
        for i in range(self.frame_count):
            self.gif.seek(i)
            frame = self.gif.copy()
            frame.save(os.path.join(self.save_path, f'frame_{i}.png'))
            print(f"Saved frame {i}")
        print("All frames saved successfully.")


if __name__=="__main__":
    g=GTA()
    g.dancing()

