# P&Lytics 📈

### Portfolio Profit & Loss Calculator from Broker Contract Notes

P&Lytics is a web-based equity investing application that automatically processes broker contract-note PDFs and calculates portfolio profit and loss.

The application extracts BUY and SELL transactions, stores them in a database, applies FIFO (First In, First Out) matching, considers transaction charges, and calculates both realised and unrealised P&L.

---

## 🚀 Project Overview

Investors often receive contract notes containing multiple transactions and charges. Manually calculating profit or loss can be time-consuming and error-prone.

P&Lytics simplifies this process by providing an automated workflow:

**Upload Contract Note → Extract Transactions → Store Data → FIFO Matching → Apply Charges → Calculate P&L → Display Results**

---

## ✨ Features

- 📄 Upload broker contract-note PDF
- 🔍 Extract BUY and SELL transactions
- 💾 Store transaction data using SQLite
- 🔄 FIFO-based trade matching
- 💰 Calculate realised P&L
- 📊 Calculate unrealised P&L
- 🧾 Consider BUY and SELL charges
- 📈 Support multiple FIFO lots
- 🔀 Support partial SELL transactions
- 🎁 Handle bonus shares
- ✂️ Handle stock splits
- 💹 Enter current market prices manually
- 📋 View complete transaction history
- 📑 Detailed P&L report
- 🔎 Search and filter transactions
- 📱 Responsive web interface

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Data Processing
- pdfplumber
- FIFO algorithm

### Database
- SQLite

### Development Environment
- PyCharm
- GitHub

---

## 🏗️ System Workflow


                Broker Contract Note PDF
                         ↓
                    PDF Upload
                         ↓
                   PDF Parser
                         ↓
             Transactions + Charges
                         ↓
                   SQLite Database
                         ↓
                Portfolio Engine
                         ↓
                  FIFO Matching
                         ↓
               Apply BUY Charges
                         ↓
               Apply SELL Charges
                         ↓
                  Realised P&L
                         ↓
          Remaining Portfolio Holdings
                         ↓
              Current Market Prices
                         ↓
                 Unrealised P&L
                         ↓
              Dashboard & P&L Report
