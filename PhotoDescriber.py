import Tkinter, tkFileDialog
import os
from PIL import ImageTk, Image
import csv
import shutil
import tkFont
import tkMessageBox
import imghdr
import webbrowser
import fileinput


class App:

	
	def __init__(self,master):  
	
	#master app which holds all the frames
	#Has one column and one row
	
		master.configure(bg = '#D6EBF2')
		master.rowconfigure(0,weight=1)
		master.columnconfigure(0,weight=1)
		
		'''
		The main frame which holds other frames
		and their widgets. Frame looks like this:
		
		Main frame
		_________________________________________
		|                   |                   |
		|                   |                   |
		|     Image Frame	|    Info Frame     |
		|                   |                   |
		|                   |                   |
		|___________________|___________________|                                   
		|                   |                   |
		|    Button Frame   |     Find Frame    |
		|___________________|___________________|
		|                   |                   |
		|   Input Frame     |  Image Link Frame |
		|___________________|___________________|
		
		
		'''
		
		self.frame = Tkinter.Frame(master,bg = '#D6EBF2')        
		self.frame.grid()
		
		'''
		The image frame holds the thumbnail 
		of the image to be described
		'''
		self.image_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
		self.image_frame.grid(row=0,column=0)
		
		'''
		The info frame holds the index of the photo,
		the file name, the file size and the latitude and longitude
		'''
		self.info_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
		self.info_frame.grid(row=0,column=1,padx=5,pady=30)
		
		
		'''
		The image link frame holds a button that opens
		a full size version of the image being described
		'''
		self.image_link_frame = Tkinter.Frame(self.frame,bg='#D6EBf2')
		self.image_link_frame.grid(row=2,column=1,padx=5,pady=30)
		
		
		'''
		The button frame holds the next and previous buttons,
		used to navigate between the photos
		'''
		self.button_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
		self.button_frame.grid(row=1)
		
		'''
		The find frame holds an entry panel used to input an integer
		and a button to go to the photo with that index 
		'''
		self.find_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
		self.find_frame.grid(row=1,column=1)
		
		'''
		The input frame holds boxes that can be used to add tags,
		an adress, or a description to the photo
		'''
		self.input_frame = Tkinter.Frame(self.frame,bg = '#D6EBF2')
		self.input_frame.grid(row=2)
		
		'''
		Buttons in the initial frame, the former will open a browser window
		used to select a folder of photos to be described, the later will
		open the main window using the contents of that file
		'''
		self.browse_button = Tkinter.Button(self.frame,text="   Select Folder  ",command=self.get_manifest_location, bg='#D6EBF2',fg='#2a2f30')
		self.browse_button.grid(row=0,column=0,sticky='w')
		
		self.upload_button = Tkinter.Button(self.frame,text="Describe Photos",command=self.get_manifest, bg='#D6EBF2',fg='#2a2f30')
		
		'''
		Labels in the initial frame, the former indicates the folder that has been selected,
		(this information is stored in the manifext_location variable),
		the latter is currently un-used
		'''
		self.folder_label = Tkinter.Label(self.frame,bg = '#D6EBF2',fg='#2a2f30')
		self.manifest_error_label = Tkinter.Label(self.frame,bg = '#D6EBF2',fg='#2a2f30')      
		
		self.manifest_location = None
		
		'''
		A label which will display the image selected
		'''
		self.image_label = Tkinter.Label(self.image_frame,bg = '#D6EBF2',fg='#2a2f30')
		
		'''
		The contents of the info frame: the labels are determined by the selected photo
		the entry objects are used to input co-ordinates
		'''
		self.photo_number_label = Tkinter.Label(self.info_frame,bg='#D6EBF2',fg='#2a2f30',text='')
		
		self.filename_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30',text='File Name: ')
		self.filesize_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30',text='File Size: ')
		
		self.photo_filename_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
		self.photo_filesize_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
		
		self.latitude_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
		self.latitude = Tkinter.Entry(self.info_frame,width=20)
		self.longitude_label = Tkinter.Label(self.info_frame,bg = '#D6EBF2',fg='#2a2f30')
		self.longitude = Tkinter.Entry(self.info_frame,width=20)
		
		'''
		A button linking to the full image
		'''
		self.image_link = Tkinter.Button(self.image_link_frame, text='View Photo', command=self.open_photo, bg='#EEF7F9', fg='#2a2f30')
		
		'''
		A variable used to store the number of images with descriptions
		'''
		self.description_number = 0
		
		'''
		Labels and input boxes for the input frame, one for description,
		one for tags and one for address
		'''
		self.description_label = Tkinter.Label(self.input_frame,text='Description: ', bg = '#D6EBF2',fg='#2a2f30')
		self.description = Tkinter.Text(self.input_frame,width=90,height=4,wrap='word')
		
		self.tags_label = Tkinter.Label(self.input_frame,text='Tags: ',bg = '#D6EBF2',fg='#2a2f30')
		self.tags = Tkinter.Text(self.input_frame,width=40,height=2,wrap='word')
		
		self.address_label = Tkinter.Label(self.input_frame,text='Address: ', bg = '#D6EBF2',fg='#2a2f30')
		self.address = Tkinter.Entry(self.input_frame,width=30)
		
		'''
		Navigation between the photos, all of the buttons will call the change photo function with a certain
		parameter (either 1, -1 or an inputted value)
		'''
		self.target_photo = Tkinter.Entry(self.find_frame, width=20)
		self.go_to_photo_button = Tkinter.Button(self.find_frame, text="Go to photo",command=self.set_photo, bg='#EEF7F9',fg='#2a2f30')
		
		self.next_button = Tkinter.Button(self.button_frame,text="Next",command= lambda: self.change_photo(1), bg='#EEF7F9',fg='#2a2f30')
		
		self.previous_button = Tkinter.Button(self.button_frame,text="Previous",command= lambda: self.change_photo(-1), bg='#EEF7F9',fg='#2a2f30')
		
		self.next_undescribed_button = Tkinter.Button(self.button_frame,text="Next Undescribed",command= lambda: self.next_undescribed_photo(), bg='#EEF7F9',fg='#2a2f30')
		
		'''
		lists of photos, information in the manifest, and indecies of undescribed photos
		'''
		self.manifest = []
		self.photos = []
		self.undescribed_photos = []
    
	'''
	Called by a button in the initial frame, creates an explorer window
	to  choose the manifest location and enables new widgets to be seen
	'''
	def get_manifest_location(self):
		self.manifest_location = tkFileDialog.askdirectory(initialdir='E:\\')
		self.folder_label.configure(text=self.manifest_location)
		self.folder_label.grid(row=0,column=1)
		self.upload_button.grid(row=1,column=0)
	
	'''
	Called by a button in the initial frame
	firstly checks the manifest for photos without a description
	while populateing the photos array with photos from the manifest
	and asks user for confirmation if there are none.
	After this it opens the main window and hides the information used in the initial window
	'''    
	def get_manifest(self):
		if not self.read_manifest():
			return
		index_number = 0       
		for row in self.manifest:
			if row[self.description_column] == "<null>":
				self.undescribed_photos.append(index_number)
			index_number += 1
			self.photos.append(row[0])
		if len(self.undescribed_photos) == 0:
			self.description_number = 0
			MB_Title = "All Photos Described"
			MB_Text = "All files in the selected folder already have a description set. Continue?"
			result = tkMessageBox.askyesno(title = MB_Title, message=MB_Text)
			if not result:
				root.quit()
		else:
			self.description_number = self.undescribed_photos[0]
		self.browse_button.grid_forget()
		self.upload_button.grid_forget()
		self.folder_label.grid_forget() 
		self.display_page()       
		
	'''
	Called by get_manifest and go_to_photo
	Loads the main page with infomation dependant on the selected photo
	(stored in the description_number variable)

    '''    
	def display_page(self):        
		number_of_photos = len(self.photos)
        
		if self.description_number == 0:            
			self.previous_button.grid_forget()
			self.next_button.grid(row=0,column=3,sticky='w')
			self.next_undescribed_button.grid(row=0, column = 6, sticky='w')			
		elif self.description_number == number_of_photos - 1:           
			self.next_button.grid_forget()
			self.next_undescribed_button.grid_forget()
			self.previous_button.grid(row=0,column=0,sticky='e')
		else:
			self.next_undescribed_button.grid(row=0, column = 6, sticky='w')
			self.next_button.grid(row=0,column=3,sticky='w')
			self.previous_button.grid(row=0,column=0,sticky='e')
		
		self.target_photo.grid(row=0, column=3, sticky='w')
		self.go_to_photo_button.grid(row=0, column=3, sticky='e')
            
		for row in self.manifest:            
			if self.photos[self.description_number] in row:                
				if row[self.description_column]=='<null>':
					self.description.insert('1.0',"A photograph of ")
				else:
					self.description.insert('1.0',row[self.description_column])
                
				if self.address_column != '<null>':
					if row[self.address_column] != "<null>":                
						self.address.insert(0,row[self.address_column])
					else:
						self.address.insert(0,"")
                
				if row[self.tags_column] != "<null>":
					self.tags.insert('1.0',row[self.tags_column])
				else:
					self.tags.insert(1.0,"")
                
                if self.position_column != '<null>':
					if row[self.latitude_column] != "<null>":
						self.latitude.insert(0,row[self.latitude_column])
					else:
						self.latitude.insert(0,"")
					
					if row[self.longitude_column] != "<null>":
						self.longitude.insert(0,row[self.longitude_column])
					else:
						self.longitude.insert(0,"")
                

        
		self.image_link.grid(row=0,column=0)  
		self.photo_number_text = 'Photo ' + str(self.description_number + 1) + " of " + str(number_of_photos)
		
		self.photo_number_label.configure(text=self.photo_number_text)
		self.photo_number_label.grid(row=0,column=0,columnspan=2,sticky='nw')
        
		self.filename_label.grid(row=1,column=0,sticky='nw')
		self.filesize_label.grid(row=2,column=0,sticky='nw')
        
		self.photo_filename_label.configure(text=self.photos[self.description_number])
		self.photo_filename_label.grid(row=1,column=1,sticky='nw')
		
		self.photo_filesize_label.configure(text=self.get_file_size())
		self.photo_filesize_label.grid(row=2,column=1,sticky='nw')
		
		
		if self.position_column != '<null>':
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
		
		if self.address_column != '<null>':
			self.address_label.grid(row=1,column=2,sticky='nsw',pady=5)
			self.address.grid(row=1,column=3,sticky='nsw',pady=5)
        
		self.display_thumbnail()
    
	'''
	Called by display_page
	determines the file size in bytes of the current photo
	and returns that as a value
	'''    
	def get_file_size(self):
		current_photo = self.manifest_location + "/" + self.photos[self.description_number]
		bytes = os.stat(current_photo).st_size
		file_size = get_file_size(bytes)
		return file_size
		
	def display_thumbnail(self):
		current_image = self.photos[self.description_number]        
		#opens the current image
		self.img = Image.open(self.manifest_location + "/" + current_image)        
		
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
		     
	def change_photo(self,value):        #"value" is either 1 or -1 depending on the button
		#goes to either the next or previous photo in the list depending on which button is pressed
		self.go_to_photo(self.description_number + value)
		
	def go_to_photo(self, index):
		prevdesc = self.manifest[self.description_number][self.description_column] #checks if description was null before saving
		#sets the current photo to the specified index number
		if len(self.description.get('1.0','end').strip()) < 20:
			#If the user has not entered a long enough description, this message box confirms if they want to leave it
			MB_Title = "No Description"
			MB_Text = "Are you sure you want to leave the current photo without adding a comprehensive description?"
			result = tkMessageBox.askyesno(MB_Title, MB_Text)
			if not result:
				#If they click no, the function cancels itself
				return
			self.undescribed_photos.append(self.description_number)
			self.undescribed_photos.sort()\
		#Removes the index from undescribed photos if a description has been added
		elif prevdesc == "<null>":
			self.undescribed_photos.remove(self.description_number)
		self.save_description()
		#shows a message box if a description is entered for the last photo that didn't have one
		if len(self.undescribed_photos) == 0 and prevdesc == "<null>":
			MB_Title = "All Photos Described"
			MB_Text = "You have just described the final photo in the folder. Continue?"
			result = tkMessageBox.askyesno(title = MB_Title, message=MB_Text)
			#if the user doesn't want to continue, the app closes itself
			if not result:
				root.quit()
		#Then the next photo is set
		self.description_number = index
		self.display_page()
		
	def next_undescribed_photo(self):
		#finds the next index in the undescribed photos array
		for index in self.undescribed_photos:
			if index > self.description_number:
				self.go_to_photo(index)
				return
		MB_Title = "Can't find Another"
		MB_Text = "There are no undescribed photos after this one"
		tkMessageBox.showerror(MB_Title, MB_Text)
		
	def set_photo(self):
		#gets the number from the input box as a reference to the photo number
		try:
			self.photo_inputted = int(self.target_photo.get())-1
			self.target_photo.delete(0, "end")
		except Exception,e:
			#If the number is invalid then an error pops up
			tkMessageBox.showerror("Validation Error", "Input must be an integer")
		if 0 <= self.photo_inputted < len(self.photos):
			#If the number fits in the list length, it goes to that photo
			self.go_to_photo(self.photo_inputted)
		else:
			tkMessageBox.showerror("Validation Error", "Failed to go to page, you must input a valid integer no greater than the number of photos")
		
	def write_manifest(self):        
		#writes to the manifest based on the app's instance of it
		file = open(self.manifest_location + '/manifest.csv','wb')
		
		csvwriter = csv.writer(file)        
		csvwriter.writerow(self.header)
		for row in self.manifest:            
			csvwriter.writerow(row)
		file.close()
		
	def save_description(self):
		#gets all the values inputted in the input boxes
		self.description_inputted = self.description.get('1.0','end').strip()        
		self.tags_inputted = self.tags.get('1.0','end').strip()
		self.address_inputted = self.address.get()
		self.latitude_inputted = self.latitude.get()
		self.longitude_inputted = self.longitude.get()
		
		#references the current photo in a variable
		self.current_row = self.manifest[self.description_number]
		file_size = self.get_file_size()
		
		#handles empty input boxes and converts the values to something usable by the manifest
		if self.latitude_inputted != '' and self.longitude_inputted != '':
			self.position = self.latitude_inputted + ', ' + self.longitude_inputted + ' (estimate)'
		else:
			self.position = '<null>'
			self.latitude_inputted = '<null>'
			self.longitude_inputted = '<null>'
		
		if len(self.address_inputted) == 0:
			self.address_inputted = '<null>'

		if self.description_inputted != 'A photograph of':
			self.current_row[self.header_index("part/field_dc_description")] = self.description_inputted
		else:
			self.current_row[self.header_index("part/field_dc_description")] = '<null>'
        
		if self.tags_inputted != '':
			self.tags_inputted = self.tags_inputted
		else:
			self.tags_inputted = "<null>"
		
        #saves the inputted values onto the app's instance of the manifest
		self.current_row[self.tags_column] = self.tags_inputted
		if self.address_column != '<null>':
			self.current_row[self.address_column] = self.address_inputted
		if self.position_column != '<null>':
			self.current_row[self.latitude_column] = self.latitude_inputted
			self.current_row[self.longitude_column] = self.longitude_inputted
			self.current_row[self.position_column] = self.position
        
        #saves the app's manifest instance onto the file
		self.manifest[self.description_number] = self.current_row
		self.write_manifest()
        
        #empties the input boxes
		self.description.delete('1.0','end')
		self.tags.delete('1.0','end')
		self.address.delete(0,len(self.address_inputted))
		self.latitude.delete(0,len(self.latitude_inputted))
		self.longitude.delete(0,len(self.longitude_inputted))
	
	def read_manifest(self):
		try:
			#opens the manifest file
			file = open(self.manifest_location + '/manifest.csv','rb')               
		except IOError:
			#Cancels the function when no manifest can be found and displays an error message
			MB_Title = "Missing Manifest"
			MB_Text = "There is no valid manifest in the selected folder. Please create one and try again."
			tkMessageBox.showerror(MB_Title, MB_Text)
			return False
		csvreader= csv.reader(file)
		#saves the file's manifest data to a local instance
		for number, row in enumerate(csvreader):            
			exist = ""
			try:
				exist = Image.open(self.manifest_location + "/" + row[0])
			except Exception, e:
				exist = ""
			if number == 0:
				self.header = row
				self.header_index = self.header.index            
			elif exist != "":
				self.manifest.append(row)
				
		try:
			#finds the relavent header fields in the manifest files and references them
			self.description_column = self.header_index("part/field_dc_description")
			self.address_column = self.header_index("#address/field_dc_title")
			self.tags_column = self.header_index("part/field_part_tags")
			self.latitude_column = self.header_index("position/field_latitude")
			self.longitude_column = self.header_index("position/field_longitude")
			self.position_column = self.header_index("#position/field_dc_title")
		except ValueError:
			#If the correct headers can't be found, the local manifest is emptied and the function terminates
			MB_Title = "Invalid Manifest"
			MB_Text = "The manifest in the selected folder is not formatted correctly. Please reformat or delete it and try again."
			tkMessageBox.showerror(MB_Title, MB_Text)
			self.manifest = []
			return False
		return True
		
	def delete_thumbnails(self):        
    	#gets rid of the temporary thumbnails and the folder that contained them if it exists
		try:
			shutil.rmtree(self.thumbnail_folder)
			root.destroy()
		except:
			root.destroy()
            
	def open_photo(self):
    	#opens the image file for the currently set photo
		webbrowser.open(self.manifest_location + "/" + self.photos[self.description_number])

    
def get_file_size(num):        
	#calculates the size of a file and returns the value
	for x in ['bytes','KB','MB','GB','TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
       	num /= 1024.0        

 
#runs the client code          
root = Tkinter.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW",app.delete_thumbnails)
root.mainloop()
