import numpy as np
import pandas as pd

data = np.load('d:/Top2Vec/data/embeddings/embeddings_todos.npz', allow_pickle=True)

print("Claves en NPZ:", list(data.keys()))

# Revisar metadata
print("\n=== Explorando metadata ===")
metadata = data['metadata'].item()  # .item() para extraer el dict
print("Tipo:", type(metadata))
if isinstance(metadata, dict):
    print("Claves en metadata:", list(metadata.keys()))
    
    if 'pub_date' in metadata:
        print("\n=== pub_date encontrado en metadata ===")
        pub_dates = metadata['pub_date']
        print("Primeras 10 pub_dates:", pub_dates[:10])
        print("Tipo:", type(pub_dates[0]) if len(pub_dates) > 0 else "vacío")
        
        # Intentar convertir a datetime
        try:
            dates_converted = pd.to_datetime(pub_dates)
            print(f"\nConversión exitosa!")
            print(f"Rango de fechas: {dates_converted.min()} - {dates_converted.max()}")
            print(f"Años disponibles: {dates_converted.min().year} - {dates_converted.max().year}")
        except Exception as e:
            print(f"\nError al convertir: {e}")
    else:
        print("\nNO HAY 'pub_date' en metadata. Claves disponibles:", list(metadata.keys()))
else:
    print("\nMetadata no es diccionario:", metadata)
