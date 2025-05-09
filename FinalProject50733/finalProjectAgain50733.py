import numpy as np 
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import time 

infectionRate = .30 
mortalityRate = .60
recoveryLength = 90
bounds = [400, 400]
interactionDistance = 16
personalSpace = 15

class Person:
    def __init__(self, healthStatus, position, velocity, masked=False):
        self.position = np.array(position, dtype = float)
        self.velocity = np.array(velocity, dtype = float)
        self.healthStatus = healthStatus
        self.alive = True 
        self.immune = False 
        self.infectionTime = 0
        self.masked = masked 
    
    def move(self, bounds, population):
        if not self.alive:
            return 
        
        for other in population:
            if other is not self and other.alive:
                dx = self.position[0] - other.position[0]
                dy = self.position[1] - other.position[1]
                distance = (dx**2 + dy**2)**0.5

                if distance < personalSpace and distance > 0: 
                    #normalzing incase of weirdness
                    dx /= distance 
                    dy /= distance   

                    self.velocity[0] += dx
                    self.velocity[1] += dy

        speed = (self.velocity[0]**2 + self.velocity[1]**2)**0.5
        maxSpeed = 2
        if speed > maxSpeed: 
            self.velocity[0] = (self.velocity[0]/ speed ) * maxSpeed
            self.velocity[1] = (self.velocity[1]/ speed ) * maxSpeed
        
        newX = self.position[0] + self.velocity[0]
        newY = self.position[1] + self.velocity[1]

        if newX < 0 or newX > bounds[0]:
            self.velocity[0] *= -1
            newX = max(0, min(newX, bounds[0]))

        if newY < 0 or newY > bounds[0]:
            self.velocity[1] *= -1
            newY = max(0, min(newY, bounds[1]))

        self.position[0] = newX
        self.position[1] = newY

    def getInfected(self):
        if self.healthStatus == 'healthy' and not self.immune:
            chance = infectionRate * (0.1 if self.masked else 1.0)
            if np.random.rand() < chance:
                self.healthStatus = 'infected'

    def updateHealth(self):
        if self.healthStatus == 'infected':
            self.infectionTime += 1

            if 80 <= self.infectionTime <= recoveryLength:
                mortalityChance = mortalityRate * (1 - (self.infectionTime / recoveryLength))
                if np.random.random() < mortalityChance:
                    self.healthStatus = 'dead'
                    self.alive = False

        # If recoveryTime has passed, person recovers
            elif self.infectionTime >= recoveryLength:
                self.healthStatus = 'recovered'
                self.immune = True


class DiseaseSimulation:
    def __init__(self, populationTotal = 200, initialInfected = 1, maskingEnabled = False):
        self.population = []
        self.populationTotal = populationTotal
        self.bounds = bounds 
        self.hours = 0
        self.stats = {'healthy': [populationTotal - initialInfected], 'infected': [initialInfected], 'recovered' : [0], 'dead' : [0], 'masked' : [0]}

        for _ in range(populationTotal):
            position = np.random.rand(2) * self.bounds
            velocity = (np.random.rand(2) - 0.5)*10
            masked = np.random.rand() < 0.5 if maskingEnabled else False
            self.population.append(Person('healthy', position, velocity, masked))

            for i in range(initialInfected):
                self.population[i].healthStatus = 'infected'

    def interaction(self):
        for i, personA in enumerate(self.population):
            if personA.healthStatus != 'infected':
                continue
            for j, personB in enumerate(self.population):
                if i != j and personB.healthStatus == 'healthy' and not personB.immune:
                    if np.linalg.norm(personA.position - personB.position) < interactionDistance:
                        personB.getInfected()
    
    def update(self):
        for person in self.population:
            person.move(self.bounds, self.population)
            person.updateHealth()

        self.interaction()
        self.hours += 1

        healthy = 0
        infected = 0 
        recovered = 0 
        dead = 0 

        for person in self.population:
            if person.healthStatus == 'healthy':
                healthy += 1
            elif person.healthStatus == 'infected':
                infected += 1
            elif person.healthStatus == 'recovered':
                recovered += 1
            elif person.healthStatus == 'dead':
                dead += 1

        self.stats['healthy'].append(healthy)
        self.stats['infected'].append(infected)
        self.stats['recovered'].append(recovered)
        self.stats['dead'].append(dead)

        return infected > -1
    
    def run(self, maxHours = 500):
        while self.hours < maxHours:
            if not self.update():
                break

        return self.stats
    
def runComparison(populationTotal = 200, initialInfected =1, maxHours = 500):
    simWithMasks = DiseaseSimulation(populationTotal, initialInfected, maskingEnabled= True)
    statsWithMask = simWithMasks.run(maxHours)

    simNoMasks = DiseaseSimulation(populationTotal, initialInfected, maskingEnabled= False)
    statsNohMask = simNoMasks.run(maxHours)

    timeWithMasks = range(len(statsWithMask['healthy']))

    timeNoMasks = range(len(statsNohMask['healthy']))


 
    
    
    simWithMasks = DiseaseSimulation(populationTotal, initialInfected, maskingEnabled=False)
    statsNohMask = simNoMasks.run(maxHours)
    plt.figure(figsize=(10, 6))
    plt.plot(timeWithMasks, statsWithMask['dead'], label = "Deaths with masks")
    plt.plot(timeNoMasks, statsNohMask['dead'], label = "Deaths without masks")
    plt.xlabel('hours')
    plt.ylabel('deaths')
    plt.title('Deaths with and without masks')
    plt.legend()
    plt.show()

runComparison(populationTotal= 200, initialInfected= 1, maxHours = 500)

def runSim():
    sim = DiseaseSimulation(populationTotal= 200, initialInfected= 1, maskingEnabled= False)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (15, 6))

    ax1.set_xlim(0, bounds[0])
    ax1.set_ylim(0, bounds[1])
    ax1.set_title('Pandemic Simulation')

    ax2.set_title('Population Stats Graph')
    ax1.set_xlim(0, 300)
    ax1.set_ylim(0, len(sim.population))
    

    lines = {'healthy': ax2.plot([], [], 'pink', label= 'Healthy')[0], 
             'infected': ax2.plot([], [], 'red', label= 'Infected')[0],
             'recovered': ax2.plot([], [], 'green', label= 'Recovered')[0],
             'dead': ax2.plot([], [], 'black', label= 'Dead')[0],
             'masked': ax2.plot([], [], 'orange', label= 'Masked')[0],}
    
    ax2.legend()
    statusText = ax1.text(5, 95, '')
    
    def update(frame):
        sim.update()

        ax1.clear()
        ax1.set_xlim(0, bounds[0])
        ax1.set_ylim(0, bounds[1])
        colors = {'healthy': 'pink', 'infected': 'red', 'recovered': 'green', 'dead': 'black' }

        for person in sim.population:
            color = colors[person.healthStatus]
            marker = 's' if person.masked else 'o'
            ax1.scatter(person.position[0], person.position[1], color = color, marker = marker )

        for g in ['healthy', 'infected', 'recovered', 'dead']:
            x_data = list(range(len(sim.stats[g])))
            y_data = sim.stats[g]
            lines[g].set_data(x_data, y_data)

        ax2.set_xlim(0, max(300, len(sim.stats['healthy']) + 10))
        ax2.set_ylim(0, sim.populationTotal)
    
        
        for f in lines:
            ax2.draw_artist(lines[f])

        statusText.set_text(f'Hour: {sim.hours}')
        return list(lines.values()) + [statusText]
    
    ani = animation.FuncAnimation(fig, update, frames = 500, interval = 200, blit = False)
    plt.show()
    return ani

if __name__ == "__main__":
    start = time.time()
    runSim()
    end = time.time()
    print(end - start)


