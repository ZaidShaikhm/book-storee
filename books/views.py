# books/views.py

import json
from bson import ObjectId
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .mongo import get_col


# ── helper: convert ObjectId to str ──────────────────────────────
def fix(doc):
    if doc is None:
        return None
    doc['id'] = str(doc.pop('_id'))
    return doc

def fix_all(docs):
    return [fix(d) for d in docs]


# ── Seed sample data if collections are empty ────────────────────
def seed():
    books = get_col('books')
    customers = get_col('customers')
    orders = get_col('orders')

    if books.count_documents({}) == 0:
        books.insert_many([
            {'title': 'Java Programming',              'author': 'James Gosling',       'price': 450, 'stock': 20},
            {'title': 'Python Cookbook',               'author': 'David Beazley',        'price': 550, 'stock': 8 },
            {'title': 'MongoDB: The Definitive Guide', 'author': 'Kristina Chodorow',    'price': 620, 'stock': 3 },
            {'title': 'Clean Code',                    'author': 'Robert C. Martin',     'price': 499, 'stock': 15},
            {'title': 'Design Patterns',               'author': 'Gang of Four',         'price': 780, 'stock': 0 },
            {'title': 'The Pragmatic Programmer',      'author': 'Andrew Hunt',          'price': 530, 'stock': 12},
            {'title': 'Introduction to Algorithms',    'author': 'Thomas Cormen',        'price': 950, 'stock': 6 },
            {'title': 'Database Systems',              'author': 'Ramez Elmasri',        'price': 680, 'stock': 9 },
        ])

    if customers.count_documents({}) == 0:
        customers.insert_many([
            {'name': 'Rahul Sharma', 'email': 'rahul@gmail.com', 'phone': '9876543210'},
            {'name': 'Priya Patel',  'email': 'priya@gmail.com', 'phone': '9123456789'},
            {'name': 'Amit Verma',   'email': 'amit@gmail.com',  'phone': '9988776655'},
            {'name': 'Sneha Iyer',   'email': 'sneha@gmail.com', 'phone': '8877665544'},
            {'name': 'Kiran Reddy',  'email': 'kiran@gmail.com', 'phone': '7766554433'},
        ])

    if orders.count_documents({}) == 0:
        b = {b['title']: str(b['_id']) for b in get_col('books').find()}
        c = {c['name']:  str(c['_id']) for c in get_col('customers').find()}
        orders.insert_many([
            {'customer_id': c['Rahul Sharma'], 'book_id': b['Java Programming'],         'customer': 'Rahul Sharma', 'book': 'Java Programming',         'quantity': 2, 'total_amount': 900,  'status': 'delivered' },
            {'customer_id': c['Priya Patel'],  'book_id': b['Clean Code'],               'customer': 'Priya Patel',  'book': 'Clean Code',               'quantity': 1, 'total_amount': 499,  'status': 'processing'},
            {'customer_id': c['Amit Verma'],   'book_id': b['Python Cookbook'],          'customer': 'Amit Verma',   'book': 'Python Cookbook',          'quantity': 3, 'total_amount': 1650, 'status': 'shipped'   },
            {'customer_id': c['Sneha Iyer'],   'book_id': b['Introduction to Algorithms'],'customer': 'Sneha Iyer',  'book': 'Introduction to Algorithms','quantity': 1, 'total_amount': 950,  'status': 'pending'   },
            {'customer_id': c['Kiran Reddy'],  'book_id': b['MongoDB: The Definitive Guide'],'customer':'Kiran Reddy','book':'MongoDB: The Definitive Guide','quantity':2,'total_amount':1240,'status':'processing'},
        ])


# ── Page ─────────────────────────────────────────────────────────
def index(request):
    seed()
    return render(request, 'books/index.html')


# ══════════════════════════════════════════════════════════════════
#  BOOKS
# ══════════════════════════════════════════════════════════════════

@csrf_exempt
def books_list(request):
    col = get_col('books')

    if request.method == 'GET':
        q = request.GET.get('search', '')
        query = {'$or': [
            {'title':  {'$regex': q, '$options': 'i'}},
            {'author': {'$regex': q, '$options': 'i'}},
        ]} if q else {}
        return JsonResponse(fix_all(list(col.find(query))), safe=False)

    if request.method == 'POST':
        body = json.loads(request.body)
        result = col.insert_one({
            'title':  body['title'],
            'author': body['author'],
            'price':  float(body['price']),
            'stock':  int(body['stock']),
        })
        doc = col.find_one({'_id': result.inserted_id})
        return JsonResponse(fix(doc), status=201)


@csrf_exempt
def book_detail(request, pk):
    col = get_col('books')
    try:
        oid = ObjectId(pk)
    except Exception:
        return JsonResponse({'error': 'Invalid ID'}, status=400)

    doc = col.find_one({'_id': oid})
    if not doc:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(fix(doc))

    if request.method == 'PUT':
        body = json.loads(request.body)
        col.update_one({'_id': oid}, {'$set': {
            'title':  body.get('title',  doc['title']),
            'author': body.get('author', doc['author']),
            'price':  float(body.get('price', doc['price'])),
            'stock':  int(body.get('stock',  doc['stock'])),
        }})
        return JsonResponse(fix(col.find_one({'_id': oid})))

    if request.method == 'DELETE':
        col.delete_one({'_id': oid})
        return JsonResponse({'message': 'Book deleted'})


# ══════════════════════════════════════════════════════════════════
#  CUSTOMERS
# ══════════════════════════════════════════════════════════════════

@csrf_exempt
def customers_list(request):
    col = get_col('customers')

    if request.method == 'GET':
        return JsonResponse(fix_all(list(col.find())), safe=False)

    if request.method == 'POST':
        body = json.loads(request.body)
        result = col.insert_one({
            'name':  body['name'],
            'email': body['email'],
            'phone': body['phone'],
        })
        doc = col.find_one({'_id': result.inserted_id})
        return JsonResponse(fix(doc), status=201)


@csrf_exempt
def customer_detail(request, pk):
    col = get_col('customers')
    try:
        oid = ObjectId(pk)
    except Exception:
        return JsonResponse({'error': 'Invalid ID'}, status=400)

    doc = col.find_one({'_id': oid})
    if not doc:
        return JsonResponse({'error': 'Customer not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(fix(doc))

    if request.method == 'PUT':
        body = json.loads(request.body)
        col.update_one({'_id': oid}, {'$set': {
            'name':  body.get('name',  doc['name']),
            'email': body.get('email', doc['email']),
            'phone': body.get('phone', doc['phone']),
        }})
        return JsonResponse(fix(col.find_one({'_id': oid})))

    if request.method == 'DELETE':
        col.delete_one({'_id': oid})
        return JsonResponse({'message': 'Customer deleted'})


# ══════════════════════════════════════════════════════════════════
#  ORDERS
# ══════════════════════════════════════════════════════════════════

@csrf_exempt
def orders_list(request):
    col = get_col('orders')

    if request.method == 'GET':
        return JsonResponse(fix_all(list(col.find().sort('_id', -1))), safe=False)

    if request.method == 'POST':
        body     = json.loads(request.body)
        books    = get_col('books')
        customers = get_col('customers')

        try:
            book_oid     = ObjectId(body['book_id'])
            customer_oid = ObjectId(body['customer_id'])
        except Exception:
            return JsonResponse({'error': 'Invalid ID'}, status=400)

        book     = books.find_one({'_id': book_oid})
        customer = customers.find_one({'_id': customer_oid})
        if not book:     return JsonResponse({'error': 'Book not found'}, status=404)
        if not customer: return JsonResponse({'error': 'Customer not found'}, status=404)

        qty = int(body['quantity'])
        if book['stock'] < qty:
            return JsonResponse({'error': f"Insufficient stock. Available: {book['stock']}"}, status=400)

        total = book['price'] * qty
        result = col.insert_one({
            'customer_id': str(customer_oid),
            'book_id':     str(book_oid),
            'customer':    customer['name'],
            'book':        book['title'],
            'quantity':    qty,
            'total_amount': total,
            'status':      'pending',
        })

        # deduct stock
        books.update_one({'_id': book_oid}, {'$inc': {'stock': -qty}})

        doc = col.find_one({'_id': result.inserted_id})
        return JsonResponse(fix(doc), status=201)


@csrf_exempt
def order_detail(request, pk):
    col = get_col('orders')
    try:
        oid = ObjectId(pk)
    except Exception:
        return JsonResponse({'error': 'Invalid ID'}, status=400)

    doc = col.find_one({'_id': oid})
    if not doc:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(fix(doc))

    if request.method == 'PATCH':
        body = json.loads(request.body)
        col.update_one({'_id': oid}, {'$set': {'status': body['status']}})
        return JsonResponse(fix(col.find_one({'_id': oid})))

    if request.method == 'DELETE':
        # restore stock
        books = get_col('books')
        try:
            book_oid = ObjectId(doc['book_id'])
            books.update_one({'_id': book_oid}, {'$inc': {'stock': doc['quantity']}})
        except Exception:
            pass
        col.delete_one({'_id': oid})
        return JsonResponse({'message': 'Order deleted, stock restored'})


# ══════════════════════════════════════════════════════════════════
#  STATS (dashboard)
# ══════════════════════════════════════════════════════════════════

def stats(request):
    books     = get_col('books')
    customers = get_col('customers')
    orders    = get_col('orders')

    revenue_agg = list(orders.aggregate([
        {'$group': {'_id': None, 'total': {'$sum': '$total_amount'}}}
    ]))
    revenue = revenue_agg[0]['total'] if revenue_agg else 0

    low_stock = fix_all(list(books.find({'stock': {'$lte': 5}}).sort('stock', 1).limit(5)))
    recent    = fix_all(list(orders.find().sort('_id', -1).limit(6)))

    return JsonResponse({
        'totalBooks':     books.count_documents({}),
        'totalCustomers': customers.count_documents({}),
        'totalOrders':    orders.count_documents({}),
        'totalRevenue':   revenue,
        'lowStock':       low_stock,
        'recentOrders':   recent,
    })


# ── Health check ─────────────────────────────────────────────────
def health(request):
    try:
        get_col('books').find_one()
        return JsonResponse({'status': 'ok', 'db': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'db': str(e)}, status=500)
