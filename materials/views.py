from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Case, When

from .models import Material, Tag, Ingredient

def explore(request):
	remove = request.GET.getlist('r')
	filter = request.GET.getlist('q')
	base_query = Material.objects.all()
	match_any = request.GET.get('or', '')
	if (match_any):
		if len(filter):
			base_query = base_query.filter(tags__id__in=filter)
	else:
		for id in filter:
			base_query = base_query.filter(tags__id=id)
	if len(remove):
		base_query = base_query.exclude(tags__id__in=remove)
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(filter)])
	filter_tags = Tag.objects.filter(id__in=filter).distinct().order_by(preserved)
	filter_tag_ids = list(filter_tags.values_list("id", flat=True))
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(remove)])
	remove_tags = Tag.objects.filter(id__in=remove).distinct().order_by(preserved)
	remove_tag_ids = list(remove_tags.values_list("id", flat=True))
	all_tags = Tag.objects.filter(category__id__in = [2,3,4])
	context = {
		"match_any": match_any,
		"remove_tag_ids": remove_tag_ids,
		"filter_tag_ids": filter_tag_ids,
		"tags": all_tags,
		"top_notes": base_query.filter(tags__id=1).distinct(),
		"middle_notes": base_query.filter(tags__id=2).distinct(),
		"bottom_notes": base_query.filter(tags__id=3).distinct(),
		"other": base_query.exclude(tags__id__in=[1,2,3]).distinct(),
	}
	return render(request, "materials/explore_view.html", context)

class MaterialListView(generic.ListView):
	template_name = "materials/material_list_view.html"
	context_object_name = "material_list"
	def get_queryset(self):
		return Material.objects.order_by("name")

class MaterialDetailView(generic.DetailView):
	model = Material
	template_name = "materials/material_detail_view.html"
	def get_context_data(self, **kwargs):
		context = super(MaterialDetailView, self).get_context_data(**kwargs)
		ingredients = Ingredient.objects.filter(parent__id = context['material'].id)
		concentration = int(self.request.GET.get('concentration', 10))
		target = float(self.request.GET.get('target', 5))
		amounts = [ingredient.concentration * ingredient.amount for ingredient in ingredients]
		total = sum(amounts)
		proportions = [amount / total for amount in amounts]
		recipe = [{
			"Ingredient": ingredients[index].material.name,
			"Material": round(proportion * concentration / 100 * target, 3),
			"Diluent": round(proportion * (1 - concentration / 100) * target, 3),
			"Diluted Total": round(proportion * target, 3),
		} for index, proportion in enumerate(proportions)]
		recipe.append({
			"Ingredient": "Totals",
			"Material": round(concentration / 100 * target, 3),
			"Diluent": round((1 - concentration / 100) * target, 3),
			"Diluted Total": round(target, 3),
		})
		print(recipe)
		context['recipe'] = recipe
		context['target'] = target
		context['concentration'] = concentration
		return context

class TagListView(generic.ListView):
	template_name = "materials/tag_list_view.html"
	context_object_name = "tag_list"
	def get_queryset(self):
		return Tag.objects.order_by("name")

class TagDetailView(generic.DetailView):
	model = Tag
	template_name = "materials/tag_detail_view.html"

