from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class Material(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	tags = models.ManyToManyField('Tag', through='Tag_materials', blank=True)
	date_created = models.DateTimeField(default=datetime.now)
	date_edited = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return self.name
	@property
	def ingredient_tags(self):
		return list({tag for ingredient in self.ingredients.all() for tag in ingredient.material.tags.all() if tag.category.id == 2})
	class Meta:
		ordering = ["name"]

class Category(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	date_created = models.DateTimeField(default=datetime.now)
	date_edited = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "Categories"
		ordering = ["name"]

class Tag(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	materials = models.ManyToManyField(Material, blank=True)
	text_color = models.CharField(max_length=30, default="white")
	background_color = models.CharField(max_length=30, default="gray")
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=datetime.now)
	date_edited = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return self.name
	class Meta:
		ordering = ["category", "name"]

class Ingredient(models.Model):
	parent = models.ForeignKey(Material, related_name='ingredients', on_delete=models.CASCADE)
	material = models.ForeignKey(Material, on_delete=models.CASCADE)
	amount = models.FloatField(
		default=1,
		validators=[
			MinValueValidator(0)
		]
	)
	concentration = models.IntegerField(
		default=10,
		validators=[
			MaxValueValidator(100),
            MinValueValidator(0)
		]
	)
	def __str__(self):
		return f"{self.material.name} ({self.concentration}%) {self.amount}"