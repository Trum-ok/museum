import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import AdminNavbar from '../components/AdminNavbar';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Exhibit } from '../components/ExhibitInterface';


function AddExhibit() {
  const [formData, setFormData] = useState<Exhibit>({
    id: 0,
    name: '',
    quantity: 0,
    obtaining: '',
    discovery: '',
    description: '',
    assignment: '',
    inventory_number: {
      number: 0,
      collection: '',
      fund: '',
    },
    image: '',
    visible: true,
  });

  // const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      console.log(token)

      const response = await fetch('http://localhost:8080/api/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
      const data = await response.json();
      console.log('Exhibit added successfully:', data);
      console.log(formData)
      // Redirect to admin page or exhibit list after successful submission
      toast.success('Экспонат успешно добавлен');
      // navigate('/admin');
      } else {
        toast.error('Ошибка при добавлении экспоната');
        console.error('Error adding exhibit:', response.statusText);
      }
    } catch (error) {
      toast.error('Ошибка при добавлении экспоната');
      console.error('Error adding exhibit:', error);
    }
  };

  return (
    <>
      <AdminNavbar />
      <ToastContainer position="bottom-right" draggable newestOnTop/>
      <div className="container">
        <div className="back_button">
          <a href="/admin/">&lt; назад</a>
        </div>
        <h1>Добавить экспонат</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">Название *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder='Название'
              />
            </div>
            <div className="form-group">
              <label htmlFor="quantity">Количество</label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                placeholder='Количество'
              />
            </div>
            <div className="form-group">
              <label htmlFor="obtaining">Способ получения</label>
              <input
                type="text"
                id="obtaining"
                name="obtaining"
                value={formData.obtaining}
                onChange={handleChange}
                placeholder='Способ получения'
              />
            </div>
            <div className="form-group">
              <label htmlFor="discovery">Место обнаружения</label>
              <input
                type="text"
                id="discovery"
                name="discovery"
                value={formData.discovery}
                onChange={handleChange}
                placeholder='Место обнаружения'
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Описание</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder='Описание'
              ></textarea>
            </div>
            <div className="form-group">
              <label htmlFor="assignment">Назначение</label>
              <input
                type="text"
                id="assignment"
                name="assignment"
                value={formData.assignment}
                onChange={handleChange}
                placeholder='Назначение'
              />
            </div>
            <h3>Инвентарный номер</h3>
            <div className="inventory-number">
              <div className="form-group">
                <label htmlFor="inventory_number"></label>
                <input
                  type="number"
                  id="inventory_number"
                  name="inventory_number"
                  value={formData.inventory_number.number}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      inventory_number: {
                        ...formData.inventory_number,
                        number: parseInt(e.target.value), // Ensure to parse the value to integer
                      },
                    })
                  }
                />
              </div>
              <div className="form-group">
                <label htmlFor="collection">Коллекция</label>
                <input
                  type="text"
                  id="collection"
                  name="collection"
                  value={formData.inventory_number.collection}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      inventory_number: {
                        ...formData.inventory_number,
                        collection: e.target.value,
                      },
                    })
                  }
                />
              </div>
              <div className="form-group">
                <label htmlFor="fund">Фонд</label>
                <input
                  type="text"
                  id="fund"
                  name="fund"
                  value={formData.inventory_number.fund}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      inventory_number: {
                        ...formData.inventory_number,
                        fund: e.target.value,
                      },
                    })
                  }
                />
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="image">Изображение</label>
              <input
                type="file"
                id="image"
                name="image"
                accept="image/*"
                onChange={handleChange}
              />
            </div>
          </div>
          <button type="submit" className='add-button'>
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="none" d="M0 0h24v24H0z"></path><path fill="currentColor" d="M11 11V5h2v6h6v2h-6v6h-2v-6H5v-2z"></path></svg>
              Добавить
            </span>
          </button>
        </form>
      </div>
    </>
  );
}

export default AddExhibit;
