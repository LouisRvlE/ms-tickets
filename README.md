sudo docker container stop ms-tickets
sudo docker container rm ms-tickets
sudo docker build -t ms-tickets .
sudo docker run -it --name ms-tickets -e PORT=5000 -p 5000:5000 -d ms-tickets

**1. Create a new ticket:**

```bash
curl -X POST http://localhost:5000/tickets -H "Content-Type: application/json" -d '{ "user_id": 1, "product_id": 2, "date": "2024-12-05T15:47:00", "total": 99.99 }'
```

**2. Get a specific ticket:**

```bash
curl http://localhost:5000/tickets/1
```

**3. Get all tickets for a user:**

```bash
curl http://localhost:5000/users/1/tickets
```

**4. Get all tickets for a product:**

```bash
curl http://localhost:5000/products/5/tickets
```
# ms-tickets
