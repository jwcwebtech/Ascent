from django.contrib import admin

from .models import Material, Tag, Ingredient, Category

class IngredientInline(admin.TabularInline):
	model = Ingredient
	fk_name = "parent"

class TagAdmin(admin.ModelAdmin):
	filter_horizontal = ('materials',)

class MaterialAdmin(admin.ModelAdmin):
	filter_horizontal = ('tags',)
	inlines = [IngredientInline]

admin.site.register(Material, MaterialAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient)
admin.site.register(Category)