from faker import Faker
from random import randint, uniform
from datetime import datetime
from app import app, db, Product

# Configuração do Faker
faker = Faker()

# Função para gerar todos os modelos disponíveis e definir shelf de forma sequencial
def generate_all_models(shelf_start=1, shelf_end=50):
    
    # Exemplos de marcas e tipos de produtos associados
    brand_models = {
        'Apple': {
            'Smartphone': [
                'iPhone 3G', 'iPhone 3GS', 'iPhone 4', 'iPhone 4S', 'iPhone 5',
                'iPhone 5C', 'iPhone 5S', 'iPhone 6', 'iPhone 6 Plus', 'iPhone 6S',
                'iPhone 6S Plus', 'iPhone SE', 'iPhone 7', 'iPhone 7 Plus', 'iPhone 8',
                'iPhone 8 Plus', 'iPhone X', 'iPhone XS', 'iPhone XS Max', 'iPhone XR',
                'iPhone 11', 'iPhone 11 Pro', 'iPhone 11 Pro Max', 'iPhone SE (2nd generation)',
                'iPhone 12', 'iPhone 12 Mini', 'iPhone 12 Pro', 'iPhone 12 Pro Max',
                'iPhone 13', 'iPhone 13 Mini', 'iPhone 13 Pro', 'iPhone 13 Pro Max',
                'iPhone 14', 'iPhone 14 Plus', 'iPhone 14 Pro', 'iPhone 14 Pro Max'
            ],
            'Tablet': [
                'iPad', 'iPad 2', 'iPad 3rd generation', 'iPad 4th generation', 'iPad Air',
                'iPad Air 2', 'iPad Mini', 'iPad Mini 2', 'iPad Mini 3', 'iPad Mini 4',
                'iPad Pro 9.7-inch', 'iPad Pro 10.5-inch', 'iPad Pro 11-inch (1st generation)',
                'iPad Pro 11-inch (2nd generation)', 'iPad Pro 12.9-inch (1st generation)',
                'iPad Pro 12.9-inch (2nd generation)', 'iPad Pro 12.9-inch (3rd generation)',
                'iPad Pro 12.9-inch (4th generation)', 'iPad Pro 12.9-inch (5th generation)',
                'iPad Air (3rd generation)', 'iPad Air (4th generation)', 'iPad Mini (5th generation)',
                'iPad Mini (6th generation)', 'iPad (5th generation)', 'iPad (6th generation)',
                'iPad (7th generation)', 'iPad (8th generation)', 'iPad (9th generation)'
            ],
            'Laptop': [
                'MacBook', 'MacBook (Retina, 12-inch, Early 2015)', 'MacBook (Retina, 12-inch, Early 2016)',
                'MacBook (Retina, 12-inch, 2017)', 'MacBook Air', 'MacBook Air (11-inch, Early 2014)',
                'MacBook Air (11-inch, Early 2015)', 'MacBook Air (13-inch, Early 2014)',
                'MacBook Air (13-inch, Early 2015)', 'MacBook Air (Retina, 13-inch, 2018)',
                'MacBook Air (Retina, 13-inch, 2019)', 'MacBook Air (M1, 2020)', 'MacBook Air (M2, 2022)',
                'MacBook Pro 13-inch', 'MacBook Pro 13-inch (Retina, Early 2015)', 'MacBook Pro 13-inch (2016)',
                'MacBook Pro 13-inch (2018)', 'MacBook Pro 13-inch (2019)', 'MacBook Pro 13-inch (M1, 2020)',
                'MacBook Pro 14-inch (M1 Pro, 2021)', 'MacBook Pro 15-inch', 'MacBook Pro 15-inch (Retina, Mid 2015)',
                'MacBook Pro 16-inch (2019)', 'MacBook Pro 16-inch (M1 Max, 2021)', 'MacBook Pro 16-inch (2023)'
            ],
            'Smartwatch': [
                'Apple Watch (1st generation)', 'Apple Watch Series 1', 'Apple Watch Series 2',
                'Apple Watch Series 3', 'Apple Watch Series 4', 'Apple Watch Series 5',
                'Apple Watch SE', 'Apple Watch Series 6', 'Apple Watch Series 7',
                'Apple Watch Series 8', 'Apple Watch Ultra', 'Apple Watch SE (2nd generation)'
            ],
            'Headphones': [
                'AirPods', 'AirPods (2nd generation)', 'AirPods (3rd generation)',
                'AirPods Pro', 'AirPods Pro (2nd generation)', 'AirPods Max',
                'Beats Studio3 Wireless', 'Beats Solo Pro', 'Beats Fit Pro',
                'Beats Powerbeats Pro', 'Beats Flex', 'Beats EP'
            ]
        }
    }
    
    # Inicializar contador para warehouse_shelf
    current_shelf = shelf_start

    # Itera sobre todos os modelos e insere na base de dados
    for brand, product_categories in brand_models.items():
        for product_type, models in product_categories.items():
            for model in models:
                ref = faker.unique.bothify(text='???-#####')
                name = model  # Usar o modelo real para o nome do produto
                buy_price = round(uniform(100, 1000), 2)
                margin = randint(50, 120)
                sell_price = round(buy_price + (buy_price * margin / 100), 2)
                stock = randint(1, 99)
                min_recommended_stock = randint(5, 50)
                last_update = ""
                update_info = "System default"
                warehouse_section = "A"
                status = "Active"

                # Criação do produto sem qr_code_path
                product = Product(
                    ref=ref,
                    qr_code_path="",  # Placeholder vazio
                    name=name,  # Nome com o modelo real
                    product_type=product_type,
                    brand=brand,
                    model=model,
                    buy_price=buy_price,
                    sell_price=sell_price,
                    margin=margin,
                    stock=stock,
                    min_recommended_stock=min_recommended_stock,
                    last_update=last_update,
                    update_info=update_info,
                    warehouse_section=warehouse_section,
                    warehouse_shelf=current_shelf,  # Shelf sequencial
                    status=status
                )
                
                db.session.add(product)
                db.session.commit()  # Commit para gerar o ID

                # Atualiza o qr_code_path com o ID gerado
                product.qr_code_path = f"http://147.79.102.137:5000/product-page/{product.id}"
                db.session.commit()

                # Incrementa a shelf e reinicia se passar do shelf_end
                current_shelf += 1
                if current_shelf > shelf_end:
                    current_shelf = shelf_start
    
    print("Todos os produtos foram gerados e inseridos com sucesso!")

# Exemplo de uso:
if __name__ == "__main__":
    with app.app_context():  # Adiciona o contexto da aplicação
        generate_all_models(shelf_start=1, shelf_end=50)
