document.addEventListener('DOMContentLoaded', function() {
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