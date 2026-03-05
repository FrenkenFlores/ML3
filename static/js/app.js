document.addEventListener('DOMContentLoaded', function() {
    // Dashboard functionality
    const addRawDataBtn = document.getElementById('addRawDataBtn');
    const downloadAllBtn = document.getElementById('downloadAllBtn');
    const datasetCards = document.querySelectorAll('.dataset-card');
    const rawdataItems = document.querySelectorAll('.rawdata-item');

    // Add Raw Data functionality
    if (addRawDataBtn) {
        addRawDataBtn.addEventListener('click', function() {
            // Redirect to upload page or show modal
            window.location.href = '/upload-rawdata';
        });
    }

    // Download All functionality
    if (downloadAllBtn) {
        downloadAllBtn.addEventListener('click', function() {
            // Implement download all datasets functionality
            alert('Download all datasets feature coming soon!');
        });
    }

    // Dataset card interactions
    datasetCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // If clicking on a button, don't trigger card click
            if (e.target.tagName === 'A' || e.target.classList.contains('btn')) {
                return;
            }
            // Redirect to dataset details
            const viewBtn = this.querySelector('.btn-primary');
            if (viewBtn) {
                window.location.href = viewBtn.href;
            }
        });
    });

    // Raw data item interactions
    rawdataItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // If clicking on a button, don't trigger item click
            if (e.target.tagName === 'A' || e.target.classList.contains('btn')) {
                return;
            }
            // Redirect to create dataset page
            const createBtn = this.querySelector('.btn-primary');
            if (createBtn) {
                window.location.href = createBtn.href;
            }
        });
    });

    // Add smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // API functionality (keep existing)
    const apiButton = document.querySelector('button');
    const heroSection = document.querySelector('.hero');

    apiButton.addEventListener('click', fetchData);

    function fetchData() {
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                const message = data.message;
                const version = data.data.version;
                const environment = data.data.environment;
                
                const result = `
                    <div class="api-result">
                        <h3>API Response</h3>
                        <p><strong>Message:</strong> ${message}</p>
                        <p><strong>Version:</strong> ${version}</p>
                        <p><strong>Environment:</strong> ${environment}</p>
                    </div>
                `;
                
                heroSection.insertAdjacentHTML('beforeend', result);
                apiButton.style.display = 'none';
            })
            .catch(error => {
                console.error('Error fetching API data:', error);
                alert('Failed to fetch API data. Check the console for details.');
            });
    }
    
    apiButton.addEventListener('click', fetchData);
    
    function fetchData() {
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                const message = data.message;
                const version = data.data.version;
                const environment = data.data.environment;
                
                const result = `
                    <div class="api-result">
                        <h3>API Response</h3>
                        <p><strong>Message:</strong> ${message}</p>
                        <p><strong>Version:</strong> ${version}</p>
                        <p><strong>Environment:</strong> ${environment}</p>
                    </div>
                `;
                
                heroSection.insertAdjacentHTML('beforeend', result);
                apiButton.style.display = 'none';
            })
            .catch(error => {
                console.error('Error fetching API data:', error);
                alert('Failed to fetch API data. Check the console for details.');
            });
    }
    
    // Add smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});