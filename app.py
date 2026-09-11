from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Price Monitor")


@app.get("/", response_class=HTMLResponse)
def read_dashboard(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.ProductPrice).all()

    # HTML + CSS UI Code
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Price Tracker Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .navbar {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }}
            .card {{ border: none; border-radius: 12px; transition: transform 0.2s, box-shadow 0.2s; }}
            .card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
            .badge-stock {{ background-color: #28a745; font-size: 0.8rem; padding: 5px 10px; border-radius: 20px; }}
            .price-tag {{ font-size: 1.4rem; font-weight: bold; color: #2a5298; }}
            .stats-card {{ background: white; border-left: 5px solid #2a5298; border-radius: 8px; padding: 15px; }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark mb-4 shadow">
            <div class="container">
                <a class="navbar-brand fw-bold fs-4" href="#">📊 Smart Price Monitor Dashboard</a>
            </div>
        </nav>

        <div class="container">
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="stats-card shadow-sm">
                        <small class="text-muted text-uppercase fw-bold">Total Scraped Items</small>
                        <h2 class="mb-0 text-dark fw-bold">{len(products)}</h2>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stats-card shadow-sm" style="border-left-color: #28a745;">
                        <small class="text-muted text-uppercase fw-bold">Database Status</small>
                        <h2 class="mb-0 text-success fw-bold">Neon Cloud PostgreSQL</h2>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stats-card shadow-sm" style="border-left-color: #ffc107;">
                        <small class="text-muted text-uppercase fw-bold">Automation Job</small>
                        <h2 class="mb-0 text-warning fw-bold">GitHub Actions Daily</h2>
                    </div>
                </div>
            </div>

            <h4 class="mb-3 fw-bold text-secondary">Scraped Products Overview</h4>
            <div class="row">
    """

    for item in products:
        html_content += f"""
                <div class="col-md-4 col-sm-6 mb-4">
                    <div class="card h-100 shadow-sm p-3">
                        <div class="card-body d-flex flex-column justify-content-between">
                            <div>
                                <span class="badge badge-stock text-white mb-2">{item.availability}</span>
                                <h6 class="card-title text-dark fw-bold" style="min-height: 48px;">{item.title}</h6>
                            </div>
                            <div class="mt-3">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <span class="price-tag">${item.price}</span>
                                    <small class="text-muted">ID: #{item.id}</small>
                                </div>
                                <a href="{item.url}" target="_blank" class="btn btn-outline-primary btn-sm w-100 fw-bold">View Original Product 🔗</a>
                            </div>
                        </div>
                    </div>
                </div>
        """

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


@app.get("/api/products")
def get_products_json(db: Session = Depends(get_db)):
    """API endpoint for raw JSON data"""
    products = db.query(models.ProductPrice).all()
    return {"total_items": len(products), "data": products}