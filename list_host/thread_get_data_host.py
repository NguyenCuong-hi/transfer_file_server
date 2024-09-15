import pandas as pd
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.abspath(os.path.join(current_dir, '..'))


class HostConnectionAccess:
    def __init__(self):
        self.filepath = PATH + '/list_host/HOST.csv'
        self.data = None

    def get_data(self):
        self.data = pd.read_csv(self.filepath)
        return self.data

    def create_by(self, client):
        data = self.get_data()
        if not data.empty:
            max_id = data['id'].astype(int).max()
            new_id = max_id + 1
        else:
            new_id = 1
        client_with_id = [new_id] + client[1:]
        new_data = pd.DataFrame([client_with_id], columns=data.columns)
        data = pd.concat([data, new_data], ignore_index=False)
        data.to_csv(self.filepath, index=False)

    def update_by(self, client, id):
        data = self.get_data()
        new_client = pd.DataFrame([client], columns=data.columns)

        idx = int(id)

        if idx in data['id'].values:
            index = data.index[data['id'] == idx].tolist()[0]
            for column in data.columns:
                data.at[index, column] = new_client.iloc[0][column]
            print(f"Updated record with host: {idx}")
        else:
            data = pd.concat([data, new_client], ignore_index=True)
            print(f"Added new record with host: {id}")
        data.to_csv(self.filepath, index=False)

    def delete_by(self, id):
        data = self.get_data()
        try:
            idx = int(id)
            if idx in data['id'].values:
                data = data[data['id'] != idx]
                print(f"Deleted record with id: {idx}")
            else:
                print(f"No record found with id: {idx}")
            data.to_csv(self.filepath, index=False)
        except ValueError:
            print(f"Invalid id provided: {id}")
