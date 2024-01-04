import mimetypes


from django.http import FileResponse, HttpResponseBadRequest,HttpResponse
from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

from .forms import ProductForm,ProductUpdateForm
from .models import Product, ProductAttachment



def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)

    if form.is_valid():
        obj =  form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('/products/create')
        else:
            form.add_error(None,"You must be logged in to create products.")

    context['form']= form
    return render(request,'products/create.html',context)



def product_list_view(request):
    object_list = Product.objects.all()
    return render(request,"products/list.html",{"object_list":object_list})


def product_detail_view(request,handle= None):
    obj = get_object_or_404(Product, handle = handle)
    is_owner = False
    is_owner = obj.user == request.user
    context = {"object":obj}
    if is_owner:
        form = ProductUpdateForm(request.POST or None,request.FILES or None,instance = obj)
        if form.is_valid():
            obj =  form.save(commit=False)
            obj.save()
            #return redirect('/products/create')
        context['form']= form
    return render(request,'products/detail.html',context)

def product_attachment_download_view(request,handle=None,pk=None):
    # attachment = ProductAttachment.objects.all().first()
    attachment = get_object_or_404(ProductAttachment,
                                   product__handle=handle,pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb')
    filename = attachment.file.name
    content_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream' 
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response
    # attachment = get_object_or_404(ProductAttachment,product__handle=).objects.all().first()

    # if attachment is not None and attachment.file:
    #     file = attachment.file.open(mode='rb')
    #     can_download = attachment.is_free or False
    #     if request.user.is_authenticated:
    #         can_download = True
    #     if can_download is False:
    #         return HttpResponseBadRequest()
    #     filename = attachment.file.name
    #     content_type, _ = mimetypes.guess_type(filename)
    #     response = FileResponse(file)
    #     response['Content-Type'] = content_type or 'application/octet-stream' 
    #     response['Content-Disposition'] = f'attachment;filename={filename}'
    #     return response
    # else:
    #     # Handle the case where no attachment is found or the file is None
    #     return HttpResponse("Attachment not found or file is missing.", status=404)