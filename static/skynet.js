'use strict';

const {
  Container,
  Typography,
} = MaterialUI;

function App() {
  // Declare a new state variable, which we'll call "count".
  const [count, setCount] = React.useState(0);

  return (
    <Container maxWidth="sm">
      <div style={{ marginTop: 24, }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Skynet
        </Typography>

        <p>You clicked {count} times</p>
        <button onClick={() => setCount(count + 1)}>
          Click me
        </button>
      </div>
    </Container>
  );
}

const domContainer = document.querySelector('#app');
ReactDOM.render(React.createElement(App), domContainer);
