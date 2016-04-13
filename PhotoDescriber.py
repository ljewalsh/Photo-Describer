import Tkinter, tkFileDialog
import os
from PIL import ImageTk, Image
import csv
import shutil
import tkFont
import imghdr
import webbrowser


class App:
    def __init__(self,master):  
        master.configure(bg = '#D6EBF2')
        master.rowconfigure(0,weight=1)
        master.columnconfigure(0,weight=1)
        
        self.frame = Tkinter.Frame(master,bg = '#D6EBF2')        
        self.frame.grid()
        
        self.image_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
        self.image_frame.grid(row=0,column=0)
        
        self.info_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
        self.info_frame.grid(row=0,column=1,padx=5,pady=30)
        
        self.image_link_frame = Tkinter.Frame(self.frame,bg='#D6EBf2')
        self.image_link_frame.grid(row=2,column=1,padx=5,pady=30)
        
        self.button_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
        self.button_frame.grid(row=1)
        
        self.input_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
        self.input_frame.grid(row=2)
        
        self.browse_button = Tkinter.Button(self.frame,text="   Select Folder  ",command=self.get_photo_location, bg='#D6EBF2',fg='#2a2f30')
        self.browse_button.grid(row=0,column=0,sticky='w')

        self.upload_button = Tkinter.Button(self.frame,text="Describe Photos",command=self.get_photos_list, bg='#D6EBF2',fg='#2a2f30')
        
        self.folder_label = Tkinter.Label(self.frame,bg = '#D6EBF2',fg='#2a2f30')
                
        self.photo_location = None
        self.photos = None        
        self.image_label = Tkinter.Label(self.image_frame,bg = '#D6EBF2',fg='#2a2f30')
        
        self.photo_number_label = Tkinter.Label(self.info_frame,bg='#D6EBF2',fg='#2a2f30',text='')
        
        self.filename_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30',text='File Name: ')
        self.filesize_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30',text='File Size: ')
        
        self.photo_filename_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
        self.photo_filesize_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
        
        self.latitude_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
        self.latitude = Tkinter.Entry(self.info_frame,width=20)
        self.longitude_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
        self.longitude = Tkinter.Entry(self.info_frame,width=20)
        
        self.image_link = Tkinter.Button(self.image_link_frame, text='View Photo', command=self.open_photo, bg='#EEF7F9', fg='#2a2f30')
             
        self.description_number = 0
        self.description_label = Tkinter.Label(self.input_frame,text='Description: ', bg = '#D6EBF2',fg='#2a2f30')
        self.description = Tkinter.Text(self.input_frame,width=90,height=4,wrap='word')
        
        self.tags_label = Tkinter.Label(self.input_frame,text='Tags: ',bg = '#D6EBF2',fg='#2a2f30')
        self.tags = Tkinter.Text(self.input_frame,width=40,height=2,wrap='word')
        
        self.address_label = Tkinter.Label(self.input_frame,text='Address: ', bg = '#D6EBF2',fg='#2a2f30')
        self.address = Tkinter.Entry(self.input_frame,width=40)
        
        self.next_button = Tkinter.Button(self.button_frame,text="Next",command=self.next_photo, bg='#EEF7F9',fg='#2a2f30')
        
        self.previous_button = Tkinter.Button(self.button_frame,text="Previous",command=self.previous_photo, bg='#EEF7F9',fg='#2a2f30')
        
        self.manifest = []
        
    def get_photo_location(self):
        self.photo_location = tkFileDialog.askdirectory(initialdir='U:\\bulk\quakestudies\content')
        self.folder_label.configure(text=self.photo_location)
        self.folder_label.grid(row=0,column=1)
        self.upload_button.grid(row=1,column=0)
        
    def get_photos_list(self):
        #creates a list of photos
        self.photos = [ photo for photo in os.listdir(self.photo_location) if os.path.isfile(os.path.join(self.photo_location,photo)) ]        
        self.photos.sort()
        
        
        
        if 'Thumbs.db' in self.photos:
            self.photos.remove('Thumbs.db')        
        if 'manifest.csv' in self.photos:
            self.photos.remove('manifest.csv')
            self.read_manifest()            
            for row in self.manifest:                
                if self.photos[self.description_number] in row:                    
                    self.description_number = self.description_number + 1
        else:
            self.write_header()
        self.display_page()
        self.browse_button.grid_forget()
        self.upload_button.grid_forget()
        self.folder_label.grid_forget()        
        
        
    def display_page(self):        
        number_of_photos = len(self.photos) - 1        
        if self.description_number == 0:            
            if len(self.manifest) == 0:                
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
                self.description.insert('1.0',lst[5])
                self.address.insert(0,lst[1])
                self.tags.insert('1.0',lst[6])
                self.latitude.insert(0,lst[3])
                self.longitude.insert(0,lst[4])
                photo_in_lst = True
        if photo_in_lst == False:
            self.description.insert('1.0',"A photograph of ")
        
        self.image_link.grid(row=0,column=0)  
        self.photo_number_text = 'Photo ' + str(self.description_number + 1) + " of " + str(number_of_photos + 1)
        
        self.photo_number_label.configure(text=self.photo_number_text)
        self.photo_number_label.grid(row=0,column=0,columnspan=2,sticky='nw')
        
        self.filename_label.grid(row=1,column=0,sticky='nw')
        self.filesize_label.grid(row=2,column=0,sticky='nw')
        
        self.photo_filename_label.configure(text=self.photos[self.description_number])
        self.photo_filename_label.grid(row=1,column=1,sticky='nw')
        
        self.photo_filesize_label.configure(text=self.get_file_size())
        self.photo_filesize_label.grid(row=2,column=1,sticky='nw')
        
        self.latitude_label.configure(text='Latitude: ')
        self.latitude_label.grid(row=3,column=0,sticky='nw')
        self.latitude.grid(row=3, column=1)
        
        self.longitude_label.configure(text='Longitude: ')
        self.longitude_label.grid(row=4,column=0,sticky='nw')
        self.longitude.grid(row=4,column=1)
        
        self.description_label.grid(row=0,column=0,sticky='e',pady=5)
        self.description.grid(row=0,column=1,columnspan=3,sticky='nsw',pady=5)
        
        self.tags_label.grid(row=1,column=0,sticky='nse',pady=5)
        self.tags.grid(row=1,column=1,sticky='nsw',pady=5)
        
        self.address_label.grid(row=1,column=2,sticky='nsw',pady=5)
        self.address.grid(row=1,column=3,sticky='nsw',pady=5)
        
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
        
        self.thumbnail_folder = "Thumbnails/"
        self.thumbnail_location = self.thumbnail_folder + self.photos[self.description_number][:-4] + " thumbnail.jpg"
        
        if not os.path.exists(self.thumbnail_folder):
            os.makedirs(self.thumbnail_folder)          
                        
        if not os.path.exists(self.thumbnail_location):            
            hpercent = (800/float(self.img.size[1]))
            wsize = int((float(self.img.size[0])*float(hpercent)))
            #creates a thumbnail
            self.img.thumbnail((800,wsize), Image.ANTIALIAS)              
            #saves the thumbnail in the thumbnails folder
            self.img.save(self.thumbnail_location,"JPEG")        
        #turns this thumbnail into a useable image
        self.thumbnail = ImageTk.PhotoImage(Image.open(self.thumbnail_location))        
        #creates a label widget with the thumbnail image in it
        self.image_label.configure(image=self.thumbnail)
        self.image_label.grid(row=0,column=0)
        
    def next_photo(self):
        self.save_description()
        self.description_number = self.description_number + 1        
            
        self.display_page()
        
    def previous_photo(self):        
        self.save_description()        
        self.description_number = self.description_number - 1        
                
        self.display_page()
        
    def write_header(self):
        header = ['Path','Address','Position','Latitude','Longitude','Description','Tags','File Size']
        self.manifest.append(header)
        file = open(self.photo_location + '/manifest.csv','wb')
        csvwriter = csv.writer(file)        
        csvwriter.writerow(header)
        file.close()
        
    def save_description(self):
        file = open(self.photo_location + '/manifest.csv','wb')
        csvwriter = csv.writer(file)        
                
        self.description_inputted = self.description.get('1.0','end').strip()        
        self.tags_inputted = self.tags.get('1.0','end').strip()
        self.address_inputted = self.address.get()
        self.latitude_inputted = self.latitude.get()
        self.longitude_inputted = self.longitude.get()
        
        current_photo = self.photos[self.description_number]
        file_size = self.get_file_size()
        
        if self.latitude_inputted != '' and self.longitude_inputted != '' and self.latitude_inputted != '<null>' and self.longitude_inputted != '<null>':
            self.position = self.latitude_inputted + ', ' + self.longitude_inputted + ' (estimate)'
        else:
            self.position = '<null>'
            self.latitude_inputted = '<null>'
            self.longitude_inputted = '<null>'
        
        if len(self.address_inputted) == 0:
            self.address_inputted = '<null>'
        
        for lst in self.manifest:
            if current_photo in lst:
                self.manifest.remove(lst)                
        
        row = [current_photo,self.address_inputted,self.position,self.latitude_inputted,self.longitude_inputted,self.description_inputted,self.tags_inputted,file_size]
        
        self.manifest.append(row)
        
        for lst in self.manifest:                
            csvwriter.writerow(lst)
        file.close()
        self.description.delete('1.0','end')
        self.tags.delete('1.0','end')
        self.address.delete(0,len(self.address_inputted))
        self.latitude.delete(0,len(self.latitude_inputted))
        self.longitude.delete(0,len(self.longitude_inputted))
    
    def read_manifest(self):
        file = open(self.photo_location + '/manifest.csv','rb')
        csv_reader = csv.reader(file)
        for row in csv_reader:
            self.manifest.append(row)
    def delete_thumbnails(self):        
        try:
            shutil.rmtree(self.thumbnail_folder)
            root.destroy()
        except:
            root.destroy()
    def open_photo(self):
        webbrowser.open(self.photo_location + "/" + self.photos[self.description_number])
    
def get_file_size(num):		
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0        

 
          
root = Tkinter.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW",app.delete_thumbnails)
root.mainloop()
