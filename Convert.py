
result = {"Oil_Flude_RMO": "Oil_Flude", "Water_Humid_RMO": "Water_Humid", "Dust_Dirt_RMO": "Dust_Dirt", "Fiber_Microdust_RMO": "Fiber_Microdust"}
form_field = []
form_object = {}
k=[]
v=[]
k = list(result.keys())
v = list(result.values())
if len(result)>0:
    for i in range(0,len(k)):
        form_object = {}
        form_object['key'] = k[i]
        form_object['value'] = v[i]
        form_field.append(form_object)
    print(form_field)