import pygame,sys,os

class Video:

    def __init__(self,size):
        self.path = "\png"
        self.name = "capture"
        self.cnt = 0
        os.system("del \png\*.*")



    def make_png(self,screen):
        self.cnt+=1
        fullpath = "png_dead_ball\%08d.png"%self.cnt
        pygame.image.save(screen,fullpath)

    #https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
    #https://stackoverflow.com/questions/3561715/using-ffmpeg-to-encode-a-high-quality-video
    def make_mp4(self, n):
        os.system(f"ffmpeg -r 30 -i png_dead_ball\\%08d.png -vcodec mpeg4 -q:v 0 -y videos_dead_ball\movie{n}.mp4")

