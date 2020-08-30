from django import forms

from django.utils.text import slugify

from .models import Product,ProductImage

PUBLISH_CHOICES = (
	#('', ""),
	('publish', "Publish"),
	('draft', "Draft"),
)

class ProductAddForm(forms.Form):
	name = forms.CharField(label='Your Title', widget= forms.TextInput(
		attrs={
			"class": "custom-class",
			"placeholder": "Name",
		}))
	description = forms.CharField(widget=forms.Textarea(
			attrs={
				"class": "my-custom-class",
				"placeholder": "Description",
				"some-attr": "this",
			}
	)) #this might be a problem looook very !
	price  = forms.DecimalField()
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)


	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1.00:
			raise forms.ValidationError("Price must be greater than $1.00")
		elif price >= 99.99:
			raise forms.ValidationError("Price must be less than $100.00")
		else:
			return price

	def clean_title(self):
		name = self.cleaned_data.get("name")
		if len(name) > 3:
			return name
		else:
			raise forms.ValidationError("Name must be greater than 3 characters long.")



class ProductModelForm(forms.ModelForm):
	tags = forms.CharField(label='Related tags', required=False)
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)
	# description = forms.CharField(widget=forms.Textarea(
	# 		attrs={
	# 			"class": "my-custom-class",
	# 			"placeholder": "Description",
	# 			"some-attr": "this",
	# 		}
	# ))
	class Meta:
		model = Product
		fields = [
			"name",
			"description",
			"price",
			"download",
            "slug",
		]
		widgets = {
			"description": forms.Textarea(
					attrs={
						"placeholder": "New Description"
					}
				),
			"name": forms.TextInput(
				attrs= {
					"placeholder": "Name"
				}
			)
		}

	def clean(self, *args, **kwargs):
		cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
		#title = cleaned_data.get("title")
		#slug = slugify(title)
		#qs = Product.objects.filter(slug=slug).exists()
		#if qs:
		# 	raise forms.ValidationError("Title is taken, new title is needed. Please try again.")
		return cleaned_data

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1.00:
			raise forms.ValidationError("Price must be greater than $1.00")
		elif price >= 100.00:
			raise forms.ValidationError("Price must be less than $100.00")
		else:
			return price

	def clean_title(self):
		name = self.cleaned_data.get("name")
		if len(name) > 3:
			return name
		else:
			raise forms.ValidationError("Name must be greater than 3 characters long.")
