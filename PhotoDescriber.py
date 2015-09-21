import Tkinter, tkFileDialog
import os
from PIL import ImageTk, Image
import csv

max_thumbnail_size = 800, 800


class App:
    def __init__(self,master):        
        self.frame = Tkinter.Frame(master,width=200,height=100)        
        self.frame.grid()
        
        self.image_frame = Tkinter.Frame(self.frame)
        self.image_frame.grid(row=0,column=0)
        
        self.info_frame = Tkinter.Frame(self.frame)
        self.info_frame.grid(row=0,column=1,rowspan=3)
        
        self.button_frame = Tkinter.Frame(self.frame)
        self.button_frame.grid(row=1)
        
        self.input_frame = Tkinter.Frame(self.frame)
        self.input_frame.grid(row=2)
        
        self.browse_button = Tkinter.Button(self.frame,text="Select Folder",command=self.get_photo_location)
        self.browse_button.grid(row=0,column=0,sticky='w')

        self.upload_button = Tkinter.Button(self.frame,text="Describe Photos",command=self.get_photos_list)
        
        self.folder_label = Tkinter.Label(self.frame)
                
        self.photo_location = None
        self.photos = None        
        self.image_label = Tkinter.Label(self.image_frame)
        
        self.filename_label = Tkinter.Label(self.info_frame)
        self.filesize_label = Tkinter.Label(self.info_frame)
        
        self.latitude_label = Tkinter.Label(self.info_frame)
        self.latitude = Tkinter.Entry(self.info_frame,width=20)
        self.longitude_label = Tkinter.Label(self.info_frame)
        self.longitude = Tkinter.Entry(self.info_frame,width=20)
        
             
        self.description_number = 0
        self.description_label = Tkinter.Label(self.input_frame,text='Description: ')
        self.description = Tkinter.Entry(self.input_frame,width=90)
        
        self.tags_label = Tkinter.Label(self.input_frame,text='Tags: ')
        self.tags = Tkinter.Entry(self.input_frame,width=40)
        
        self.address_label = Tkinter.Label(self.input_frame,text='Address: ')
        self.address = Tkinter.Entry(self.input_frame,width=40)
        
        self.next_button = Tkinter.Button(self.button_frame,text="Next",command=self.next_photo)
        self.previous_button = Tkinter.Button(self.button_frame,text="Previous",command=self.previous_photo)
        
        self.manifest = []
        
    def get_photo_location(self):
        self.photo_location = tkFileDialog.askdirectory()
        self.folder_label.configure(text=self.photo_location)
        self.folder_label.grid(row=0,column=1)
        self.upload_button.grid(row=1,column=0)
        
    def get_photos_list(self):
        #creates a list of photos
        self.photos = [ photo for photo in os.listdir(self.photo_location) if os.path.isfile(os.path.join(self.photo_location,photo)) ]        
        if 'Thumbs.db' in self.photos:
            self.photos.remove('Thumbs.db')        
        if 'manifest.csv' in self.photos:
            self.photos.remove('manifest.csv')
            self.read_manifest()            
            for row in self.manifest:                
                if self.photos[self.description_number] in row:                    
                    self.description_number = self.description_number + 1          
        self.display_page()
        self.browse_button.grid_forget()
        self.upload_button.grid_forget()
        self.folder_label.grid_forget()
        
    def display_page(self):        
        number_of_photos = len(self.photos) - 1        
        if self.description_number == 0:            
            if len(self.manifest) == 0:
                self.description.insert(0,"A photograph of ")
                self.next_button.grid(row=0,column=3,sticky='w')                
            else:
                self.next_button.grid(row=0,column=3,sticky='w')
                self.previous_button.grid_forget()       
        elif self.description_number == number_of_photos:           
            self.next_button.grid_forget()
            self.previous_button.grid(row=0,column=0,sticky='e')            
        else:
            self.next_button.grid(row=0,column=3,sticky='w')
            self.previous_button.grid(row=0,column=0,sticky='e') 
        photo_in_lst = False
        
        for lst in self.manifest:
            if self.photos[self.description_number] in lst:                
                self.description.insert(0,lst[5])
                self.address.insert(0,lst[1])
                self.tags.insert(0,lst[6])
                self.latitude.insert(0,lst[3])
                self.longitude.insert(0,lst[4])
                photo_in_lst = True
        if photo_in_lst == False:
            self.description.insert(0,"A photograph of ")
         
        self.filename_label.configure(text='Filename: ' + self.photos[self.description_number])
        self.filename_label.grid(row=0,sticky='nw',columnspan=2)
        
        self.filesize_label.configure(text='Filesize: ' + self.get_file_size())
        self.filesize_label.grid(row=1,sticky='nw',columnspan=2)
        
        self.latitude_label.configure(text='Latitude: ')
        self.latitude_label.grid(row=2,column=0)
        self.latitude.grid(row=2, column=1)
        
        self.longitude_label.configure(text='Longitude: ')
        self.longitude_label.grid(row=3,column=0)
        self.longitude.grid(row=3,column=1)
        
        
        self.description_label.grid(row=0,column=0,sticky='e')
        self.description.grid(row=0,column=1,columnspan=3,sticky='nsw')
        
        self.tags_label.grid(row=1,column=0,sticky='nsw')
        self.tags.grid(row=1,column=1,sticky='nsw')
        
        self.address_label.grid(row=1,column=2,sticky='nsw')
        self.address.grid(row=1,column=3,sticky='nsw')
        
        self.display_thumbnail()
        
    def get_file_size(self):
        current_photo = self.photo_location + "/" + self.photos[self.description_number]
        bytes = os.stat(current_photo).st_size
        file_size = get_file_size(bytes)
        return file_size
        
    def display_thumbnail(self):
        current_image = self.photos[self.description_number]        
        #opens the current image
        self.img = Image.open(self.photo_location + "/" + current_image)        
        
        #makes thumbnail location
        self.thumbnail_location = "Thumbnails/" + self.photos[self.description_number][:-4] + " thumbnail.jpg"
        
        if not os.path.exists(self.thumbnail_location):            
            #creates a thumbnail
            self.img.thumbnail(max_thumbnail_size, Image.ANTIALIAS)              
            #saves the thumbnail in the thumbnails folder
            self.img.save(self.thumbnail_location,"JPEG")        
        #turns this thumbnail into a useable image
        self.thumbnail = ImageTk.PhotoImage(Image.open(self.thumbnail_location))        
        #creates a label widget with the thumbnail image in it
        self.image_label.configure(image=self.thumbnail)
        self.image_label.grid(row=0,column=0,columnspan=3)
        
    def next_photo(self):
        self.save_description()
        self.description_number = self.description_number + 1        
            
        self.display_page()
        
    def previous_photo(self):        
        self.save_description()        
        self.description_number = self.description_number - 1        
                
        self.display_page()
        
    def save_description(self):
        file = open(self.photo_location + '/manifest.csv','wb')
        csvwriter = csv.writer(file)        
        
        self.description_inputted = self.description.get()
        self.tags_inputted = self.tags.get()
        self.address_inputted = self.address.get()
        self.latitude_inputted = self.latitude.get()
        self.longitude_inputted = self.longitude.get()
        
        current_photo = self.photos[self.description_number]
        file_size = self.get_file_size()
        
        try:
            self.position = self.latitude + ', ' + self.logitude + ' (estimate)'
        except:
            self.position = '<null>'
        
        for lst in self.manifest:
            if current_photo in lst:
                self.manifest.remove(lst)                
        
        row = [current_photo,self.address_inputted,self.position,self.latitude_inputted,self.longitude_inputted,self.description_inputted,self.tags_inputted,file_size]
        
        if row not in self.manifest:
            self.manifest.append(row)
            csvwriter.writerow(['Path','Address','Position','Latitude','Longitude','Description','Tags','File Size'])
            for lst in self.manifest:                
                csvwriter.writerow(lst)
        file.close()
        self.description.delete(0,len(self.description_inputted))
        self.tags.delete(0,len(self.tags_inputted))
        self.address.delete(0,len(self.address_inputted))
        self.latitude.delete(0,len(self.latitude_inputted))
        self.longitude.delete(0,len(self.longitude_inputted))
    
    def read_manifest(self):
        file = open(self.photo_location + '/manifest.csv','rb')
        csv_reader = csv.reader(file)
        for row in csv_reader:
            self.manifest.append(row)
    
def get_file_size(num):		
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0        

 
          
root = Tkinter.Tk()
app = App(root)
root.mainloop()
