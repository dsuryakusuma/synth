from math import sin, pi as PI

class Node:
    def __init__(self):
        pass
    
    def ports(self):
        ports = {}
        for name in dir(self):
            attr = getattr(self, name)
            if isinstance(attr, Port):
                ports[name] = attr
        return ports
                 
class Stream:
    def sample(self, time):
        raise NotImplementedError()

class Port:
    def __init__(self, **kwargs):
        self.label = kwargs['label']

class Input(Port):
    def __init__(self, **kwargs):
        kwargs['label'] = kwargs.get('label', 'input')
        super(Input, self).__init__(**kwargs)
        self.required = kwargs.get('required', True)
        self.default_value = kwargs.get('default_value', None)
        self.stream = None
    
    def bind_stream(self, stream):
        self.stream = stream
    
    def sample(self, time):
        if self.stream is not None:
            return self.stream.sample(time)
        else:
            return self.default_value

class Output(Port, Stream):
    def __init__(self, **kwargs):
        kwargs['label'] = kwargs.get('label', 'output')
        super(Output, self).__init__(**kwargs)
        self.sample = kwargs.get('sample')

class ConstantSource(Node):
    def __init__(self, value, **kwargs):
        super(ConstantSource, self).__init__(**kwargs)
        
        def sample_output(time):
            return value
        
        self.output = Output(label='output', sample=sample_output)

class SineSource(Node):
    def __init__(self, **kwargs):
        super(SineSource, self).__init__(**kwargs)
        
        def sample_output(time):
            return sin(2 * PI * time * self.frequency.sample(time))
        
        self.frequency = Input(label='frequency')
        self.output = Output(label='output', sample=sample_output)

class SquareSource(Node):
    def __init__(self, **kwargs):
        super(SquareSource, self).__init__(**kwargs)
        
        def sample_output(time):
            return 1 if (time * self.frequency.sample(time) % 1) < 0.5 else -1
        
        self.frequency = Input(label='frequency')
        self.output = Output(label='output', sample=sample_output)

class AdderNode(Node):
    def __init__(self, **kwargs):
        super(AdderNode, self).__init__(**kwargs)
        
        def sample_output(time):
            return self.input1.sample(time) + self.input2.sample(time)
        
        self.input1 = Input(label='input 1')
        self.input2 = Input(label='input 2')
        self.output = Output(label='output', sample=sample_output)

class MultiplierNode(Node):
    def __init__(self, **kwargs):
        super(MultiplierNode, self).__init__(**kwargs)
        
        def sample_output(time):
            return self.input1.sample(time) * self.input2.sample(time)
        
        self.input1 = Input(label='input 1')
        self.input2 = Input(label='input 2')
        self.output = Output(label='output', sample=sample_output)
