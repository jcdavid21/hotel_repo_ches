import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from . import inventory_module

def inventory_spa(request):
    """
    Renders the Single Page Application (SPA) shell.
    """
    return render(request, 'inventory/inventory_spa.html')

# --- API Endpoints ---

def api_inventory_items(request):
    """
    GET /inventory/items
    Returns all items as JSON.
    """
    items = inventory_module.InventoryItem.objects.select_related('category').all().order_by('category__category_name')
    data = []
    for item in items:
        data.append({
            'id': item.item_id,
            'name': item.item_name,
            'category': item.category.category_name,
            'quantity': float(item.quantity_in_stock),
            'min_quantity': float(item.minimum_quantity),
            'cost': float(item.unit_cost) if item.unit_cost else 0,
            'is_low_stock': item.quantity_in_stock < item.minimum_quantity
        })
    return JsonResponse({'items': data})

def api_low_stock(request):
    """
    GET /inventory/low-stock
    Returns items below minimum quantity.
    """
    items = inventory_module.InventoryItem.objects.filter(quantity_in_stock__lt=F('minimum_quantity'))
    data = []
    for item in items:
        data.append({
            'id': item.item_id,
            'name': item.item_name,
            'quantity': float(item.quantity_in_stock),
            'min_quantity': float(item.minimum_quantity)
        })
    return JsonResponse({'low_stock_items': data})

@csrf_exempt
def api_add_item(request):
    """
    POST /inventory/add
    Body: { "name": "...", "quantity": 10, "category": "...", "cost": 5.0 }
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            item = inventory_module.add_item(
                item_name=body.get('name'),
                quantity=body.get('quantity'),
                category_name=body.get('category'),
                cost=body.get('cost')
            )
            if item:
                return JsonResponse({'success': True, 'message': f"Item '{item.item_name}' added."})
            return JsonResponse({'success': False, 'message': 'Failed to add item.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_update_stock(request):
    """
    POST /inventory/update
    Body: { "name": "...", "quantity": 5 } (Positive to add)
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            success = inventory_module.update_stock(
                item_name=body.get('name'),
                quantity=body.get('quantity'),
                transaction_type='adjustment',
                department='Manager'
            )
            if success:
                return JsonResponse({'success': True, 'message': 'Stock updated.'})
            return JsonResponse({'success': False, 'message': 'Update failed (Check item name or stock).'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_remove_item(request):
    """
    POST /inventory/remove
    Body: { "name": "...", "quantity": 5 } (Quantity to deduct/remove)
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            # If quantity is provided, we deduct, else could implement delete
            # Requirements say "deduct quantity" for remove endpoint usually in this context
            # Reusing update_stock with negative value
            qty = float(body.get('quantity', 0))
            success = inventory_module.update_stock(
                item_name=body.get('name'),
                quantity=-qty,
                transaction_type='removal',
                department='Manager'
            )
            if success:
                return JsonResponse({'success': True, 'message': f"Removed {qty} items."})
            return JsonResponse({'success': False, 'message': 'Removal failed.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_request_cleaning(request):
    """
    POST /inventory/request-cleaning
    Body: { "staff_name": "...", "item_name": "...", "quantity": ... }
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            success = inventory_module.request_cleaning_supplies(
                staff_name=body.get('staff_name'),
                item_name=body.get('item_name'),
                quantity_needed=float(body.get('quantity'))
            )
            if success:
                return JsonResponse({'success': True, 'message': 'Cleaning supplies approved.'})
            return JsonResponse({'success': False, 'message': 'Request denied.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_request_restaurant(request):
    """
    POST /inventory/request-restaurant
    Body: { "item_name": "...", "quantity": ... }
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            success = inventory_module.request_ingredients(
                department_name='Restaurant',
                item_name=body.get('item_name'),
                quantity_needed=float(body.get('quantity'))
            )
            if success:
                return JsonResponse({'success': True, 'message': 'Ingredients approved.'})
            return JsonResponse({'success': False, 'message': 'Request denied.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
