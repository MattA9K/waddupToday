from django import forms
from models import Entry, Comments, User_Profile
import datetime

class EntryForm(forms.ModelForm):
	
	class Meta:
		model = Entry
		fields = ('title', 'body', 'thumbnail', 'categories')
		
	def __init__(self, *args, **kwargs):
		super(EntryForm, self).__init__(*args, **kwargs)

		for fieldname in ['title', 'body', 'thumbnail', 'categories']:
			self.fields[fieldname].help_text = None
			
			
			
class EntryFormText(forms.ModelForm):
	
	class Meta:
		model = Entry
		fields = ('title', 'body', 'categories')
		
	def __init__(self, *args, **kwargs):
	    super(EntryFormText, self).__init__(*args, **kwargs)
	    
	    for fieldname in ['title', 'body', 'categories']:
			self.fields[fieldname].help_text = None
			
			
			
class EntryFormURL(forms.ModelForm):
	
	class Meta:
		model = Entry
		fields = ('title', 'body', 'categories')
		
	def __init__(self, *args, **kwargs):
	    super(EntryFormURL, self).__init__(*args, **kwargs)
	    self.fields['body'].label = "URL:"
	    self.fields['body'].help_text = "Enter a YouTube video URL or Vimeo URL (example: https://www.youtube.com/watch?v=uK367T7h6ZY, http://vimeo.com/72699930). For hashtags, put the hashtag in the title."
	    
	    for fieldname in ['title','categories']:
			self.fields[fieldname].help_text = None
		
			
		
		
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ('body',)



class User_ProfileForm(forms.ModelForm):
	class Meta:
		model = User_Profile
		fields = ('bio', 'website', 'avatar',)
		
